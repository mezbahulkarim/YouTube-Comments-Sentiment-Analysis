    # Make the prediction and get a single value from the whole list of predicted values
    y_pred = model.predict(batch_data)
    offset = 1
    pred_quality = y_pred[y_pred.size-offset]
    print("printing y_pred or total predictions: ")
    print(y_pred)
    print("-----------------------------------------------------------")
    print("Quality predicted: " + str(pred_quality))

    # Gets the actual value from the feature store -> feature group 
    wine_fg = fs.get_feature_group(name="wine", version=1)
    df = wine_fg.read() 
    print(df)                                               #Notice how batch data is the same as this, thus offset will lead to same row for true value
    true_quality = df.iloc[-offset]["quality"]
    print("Quality actual: " + str(true_quality))   

    # Make a feature group for the predicions after inferences
    monitor_fg = fs.get_or_create_feature_group(name="wine_predictions",
                                                version=1,
                                                primary_key=["datetime"],
                                                description="Wine Quality Prediction/Outcome Monitoring"
                                                )
    # Make a dataframe for current prediction and insert it to the feature "wine predictions" feature group
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'prediction': [pred_quality],
        'label': [true_quality],
        'datetime': [now],
       }
    monitor_df = pd.DataFrame(data)                                                 
    monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})           #INSERTS OUR PREDICTED vs ACTUAL 'data' value into the feature store
    
    history_df = monitor_fg.read()                                                  #SHOW recent history from wine-predictions feature group
    # Add our prediction to the history, as the history_df won't have it - 
    # the insertion was done asynchronously, so it will take ~1 min to land on App
    history_df = pd.concat([history_df, monitor_df])

    # Upload the recent history to /Resources/images in hopsworks
    df_recent = history_df.tail(4)
    dfi.export(df_recent, './wine_df_recent.png', table_conversion = 'matplotlib')
    dataset_api = project.get_dataset_api()  
    dataset_api.upload("./wine_df_recent.png", "Resources/images", overwrite=True)
    
    # These values are used as x and y values in confusion matrix later, true values are labels, predicted values are predictions
    predictions = history_df[['prediction']]
    labels = history_df[['label']]                                                  

    # Create confusion matrix
    print("Number of different wine predictions to date: " + str(predictions.value_counts().count()))
    if predictions.value_counts().count() >= 1:
        results = confusion_matrix(labels, predictions)
    
        df_cm = pd.DataFrame(results)
    
        pyplot.figure(figsize=(20, 10))
        cm = sns.heatmap(df_cm, annot=True, fmt="d")
        fig = cm.get_figure()
        fig.savefig("./wine_confusion_matrix.png")
        dataset_api.upload("./wine_confusion_matrix.png", "Resources/images", overwrite=True)
    else:
        print("Run the batch inference pipeline more than once at least") 