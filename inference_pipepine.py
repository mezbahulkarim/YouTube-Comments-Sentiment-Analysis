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

    project = hopsworks.login(api_key_value="ENTER VALUE")
    fs = project.get_feature_store()
    
    # Download the model saved 
    mr = project.get_model_registry()
    model = mr.get_model("comments_model", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/comments_model.pkl")
    
    #Get Batch Data
    feature_view = fs.get_feature_view(name="comments", version=1)
    batch_data = feature_view.get_batch_data()
    print("Printing batch data:")
    print(batch_data)
    print("-----------------------------------------------------------")

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        modal.runner.deploy_stub(stub)
        with stub.run():
            print(f.remote())           #SHOWS PRINTS

