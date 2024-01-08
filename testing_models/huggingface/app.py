
import os

os.system("python3 -m pip install --upgrade pip")
os.system("pip install httpx==0.24.1")
os.system("pip uninstall -y gradio")
os.system("pip install gradio==3.1.4")

import gradio as gr
import hopsworks
import joblib
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from googleapiclient.discovery import build
import re

config = dotenv_values(".api_key")
key_value = config["KEY"]
hopsworks_key = config["HOPSWORKS_KEY"]

youtube = build(
    'youtube',
    'v3',
    developerKey=key_value
)

project = hopsworks.login(api_key_value=hopsworks_key)
fs = project.get_feature_store()


mr = project.get_model_registry()
model = mr.get_model("comments_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/comments_model.pkl")
vectorizer = joblib.load(model_dir + "/vectorizer.pkl")
print("Model downloaded")

def get_video_id(video_link):

    # Define a regular expression pattern to match YouTube video URLs
    pattern = (
        r'(?:https?://)?(?:www\.)?'
        '(?:youtube\.com/.*?[?&]v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/e/|youtube\.com/user/[^/]+/u/0/|www\.youtube\.com/user/[^/]+/u/0/|youtube\.com/s[^/]+/|www\.youtube\.com/s[^/]+/|youtube\.com/channel/|youtube\.com/c/|youtube\.com/user/[^/]+/|youtube\.com/user/[^/]+/live/|twitch\.tv/)'
        '([^"&?/ ]{11})'
    )

    # Use re.search to find the video ID in the URL
    match = re.search(pattern, video_link)

    # If a match is found, return the video ID; otherwise, return None
    return match.group(1) if match else None


def sentiment(video_link):
    print("Calling function")
    video_id = get_video_id(video_link)
    request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100
)
    response = request.execute()

    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comment_text = ''.join(e for e in comment['textDisplay'] if (e.isalnum() or e.isspace()))
        comments.append([comment_text])

    df = pd.DataFrame(comments, columns=['comment'])
    df = df.dropna(subset=['comment'])
    comments_features = vectorizer.transform(df['comment'])
    predictions = model.predict(comments_features)
    positive_count = sum(predictions > 0)
    negative_count = sum(predictions < 0)
    total_count = len(predictions)
    positive_percentage = (positive_count / total_count) * 100
    negative_percentage = (negative_count / total_count) * 100
    return positive_count, negative_count, f"{positive_percentage:.2f}%", f"{negative_percentage:.2f}%"
        
demo = gr.Interface(
    fn=sentiment,
    title="YouTube comment sentiment analysis",
    description="Experiment with YouTube comments to predict the YouTube video sentiments.",
    allow_flagging="never",
    inputs=gr.Textbox(type="text", label="input YouTube video link",variable="video_link"),
    outputs=[
        gr.Number(label="The number of positive comments", default=0), 
        gr.Number(label="The number of negative comments", default=0),
        gr.Textbox(label="Percentage of positive comments", name="positive_percentage"),
        gr.Textbox(label="Percentage of negative comments", name="negative_percentage"),
    ],
)

demo.launch(debug=True, share=True)

