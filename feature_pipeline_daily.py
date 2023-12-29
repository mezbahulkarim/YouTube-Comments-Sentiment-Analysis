import os
import modal
from googleapiclient.discovery import build
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

LOCAL=False

if LOCAL == False:
   stub = modal.Stub("comments_daily")
   image = modal.Image.debian_slim().pip_install(["hopsworks","google-api-python-client","pandas","vaderSentiment"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       print(os.environ["HOPSWORKS_API_KEY"])
       g()


def g():
    import hopsworks
    import pandas as pd
    from googleapiclient.discovery import build

    project = hopsworks.login(api_key_value="HOPS KEY")
    fs = project.get_feature_store()

    #Youtube object
    youtube = build(
    'youtube',
    'v3',
    developerKey="YT KEY"
    )

    # Returns video id of top search result
    def search_video(query):
        request = youtube.search().list(
            part="id",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        if 'items' in response and response['items']:
            video_id = response['items'][0]['id']['videoId']
            return video_id
        else:
            return None

    # Gets first comment from video ID
    def get_comments(video_id):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=1  # Fetch only one comment for simplicity
        )

        response = request.execute()

        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            # Remove special characters from the comments
            comment_text = ''.join(e for e in comment['textDisplay'] if (e.isalnum() or e.isspace()))
            comments.append([comment_text])

        return comments

    # Search for videos related to the query
    video_id = search_video("game review")      # HARD CODED

    if video_id:
        # Fetch comments from the first search result
        comments = get_comments(video_id)
        
        # Create a DataFrame from the comments
        df = pd.DataFrame(comments, columns=['comment'])
        print("First Comment:")
        print(df['comment'].iloc[0])
        print("---------------------------------------------------------------------------------------------------")
        
        # Give sentiment score to the comment
        analyzer = SentimentIntensityAnalyzer()
        df['sentiment'] = df['comment'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
        
        # Insert into the feature group 
        fg = fs.get_feature_group(name="comments",version=1)
        fg.insert(df)

    else:
        print("No results were found!")
        return

    #comment_df = "make dataframe from comment"
    #comment_fg = fs.get_feature_group(name="comments",version=1)
    #comment_fg.insert(comment_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        modal.runner.deploy_stub(stub)
        with stub.run():
            print(f.remote())
