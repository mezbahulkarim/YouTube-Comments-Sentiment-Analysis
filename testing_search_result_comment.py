import re
import pandas as pd
from googleapiclient.discovery import build
from dotenv import dotenv_values

# Set your YouTube API key
key_value = 'YOUR_API_KEY'

# Set Key Value

config = dotenv_values(".api_key")
key_value = config["KEY"]

print(key_value)

youtube = build(
    'youtube',
    'v3',
    developerKey=key_value
)

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

# Prompt user for search query
search_query = str(input("Enter search query: "))

# Search for videos related to the query
video_id = search_video(search_query)

if video_id:
    # Fetch comments from the first search result
    comments = get_comments(video_id)

    # Create a DataFrame from the comments
    df = pd.DataFrame(comments, columns=['comment'])

    # Display the first comment
    print("First Comment:")
    print(df['comment'].iloc[0])
else:
    print("No videos found for the given query.")