# Overall this code will make inference, store predicted vs. actual in feature store and show confusion matrix, also saves images to hopsworks /Resources

#"modal token new"  ->  Link Modal Account if seeing token error
import os      
import modal 

LOCAL=False      #LOCAL=False for running on modal etc.

if LOCAL == False:
   stub = modal.Stub("testing-comments-batch")
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn==1.3.2","dataframe-image"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()

def g():
    import pandas as pd
    import hopsworks
    import joblib
    import datetime
    from PIL import Image
    from datetime import datetime
    import dataframe_image as dfi
    #from sklearn.metrics import confusion_matrix
    from matplotlib import pyplot
    import seaborn as sns
    import requests
    from sklearn.feature_extraction.text import TfidfVectorizer
    import random

    project = hopsworks.login(api_key_value="ENTER HOPSWORKS VALUE")
    fs = project.get_feature_store()
    
    # Download the model saved 
    mr = project.get_model_registry()
    model = mr.get_model("comments_model", version=2)    #REMEMBER TO CHANGE THIS TO YOUR VERSION NUMBER TO 1 IF IT'S FIRST RUN ONLY
    model_dir = model.download()

    print("------------------------------------------------------------")

    model = joblib.load(model_dir + "/comments_model.pkl")
    vectorizer = joblib.load(model_dir + "/vectorizer.pkl")
    #Get Batch Data
    feature_view = fs.get_feature_view(name="comments", version=1)
    batch_data = feature_view.get_batch_data()
    print("Printing batch data:")
    print(batch_data)
    print("-----------------------------------------------------------")

    batch_comments = batch_data['comment']
    batch_features = vectorizer.transform(batch_comments)
    predictions = model.predict(batch_features)
    print(predictions)

    # testing a single message
    message = ["i like video games"]
    print(f"the message: {message}")
    test_stuff = vectorizer.transform(message)
    output = model.predict(test_stuff)
    print("-------------------------------------------")
    print(output)
    print("RECEIVED THIS OUTPUT^ WE ARE GOOD")
   
    #  Using this index to compare the predicted value vs actual value
    total_rows = batch_data.shape[0]
    random_index = random.randint(0, total_rows-1)

    # Get actual value from feature store
    comments_fg = fs.get_feature_group(name="comments")
    df = comments_fg.read()

    # Get Predicted value and True Value
    predicted_value = predictions[predictions.size-random_index]
    true_value = df.iloc[-random_index]["sentiment"]
    print(f"Difference in prediction vs true value is {predicted_value-true_value}")

    # Feature Group to Store Predictions
    monitor_fg = fs.get_or_create_feature_group(name="comment_predictions",
                                            version=1,
                                            primary_key=["datetime"],
                                            description="Youtube Sentiment Prediction/Outcome Monitoring"
                                            )
    
    # Make a dataframe for current prediction and insert it to the feature "wine predictions" feature group
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'prediction': [predicted_value],
        'label': [true_value],
        'datetime': [now],
       }
    monitor_df = pd.DataFrame(data)
    monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False}) 

    # Show predicted history, concatenate to predicted
    history_df = monitor_fg.read()   
            # Add our prediction to the history, as the history_df won't have it - 
            # the insertion was done asynchronously, so it will take ~1 min to land on App
    history_df = pd.concat([history_df, monitor_df])

    # Upload image of predicted values
    df_recent = history_df.tail(4)
    dfi.export(df_recent, './comments_df_recent.png', table_conversion = 'matplotlib')
    dataset_api = project.get_dataset_api()  
    dataset_api.upload("./comments_df_recent.png", "Resources/images", overwrite=True)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        modal.runner.deploy_stub(stub)
        with stub.run():
            print(f.remote())           #SHOWS PRINTS

