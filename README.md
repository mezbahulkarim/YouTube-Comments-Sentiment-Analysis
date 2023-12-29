# YouTube-Comments-Sentiment-Analysis
Project work for the course ID2223. Sentiment analysis for YouTube comments and a UI to generate a positive to negative comment ratio from a YouTube video link.

Sentiment scores explained:

- -1 to less than 0 = Negative
- 0 = Neutral
- Greater than 0 and up to 1 = Positive

## Workflow

Execute the files in this order:
1. fetch_comments.ipynb
2. feature_engineering.ipynb
3. training.ipynb 
4. feature_pipeline_daily.py
5. inference_pipeline.py

## Enabling YouTube API 

- Log in to the Gmail/Google account you want to use on the browser
- Navigate to https://console.cloud.google.com
- Create new project 
- Search for API & Services
- Select Enable API & Services
- Select YouTube Data API v3 
- Enable
- Credentials
- Create API Credentials
- API Key

### Save your YouTube API Key in a ".api_key" file in the main or root directory. 

> \>cat .api_key  
KEY=PASTE_VALUE_HERE

## To label the data we will use VADER Sentiment Analysis
- Repo: https://github.com/cjhutto/vaderSentiment
- pypi link: https://pypi.org/project/vaderSentiment/

## To-Do

Separate the UI logic from the inference serving history logic. 