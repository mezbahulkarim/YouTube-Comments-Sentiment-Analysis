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
6. app.py

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

## Dataset
- The dataset used in this project consists of comments from YouTube videos. These comments were collected using the YouTube API, and the sentiment of each comment was labeled numerically using VADER. The dataset includes features such as the comment text and sentiment label.


## To-Do
- Data Collection: Utilize the YouTube API to collect comments from specific videos and implement a function to extract video IDs from YouTube video links.
- Training models: choose Random Forest Regressor model for sentiment analysis and evaluate model performance using Mean Squared Error and Root Mean Squared Error metrics.
- Deployment on Hopsworks
- Gradio Interface
- Huggingface App

## Results
- Achieved promising results in sentiment analysis with Random Forest Regression model.
- Mean Squared Error and Root Mean Squared Error were used to evaluate model performance.
- The Gradio interface provides a user-friendly way to interact with the sentiment analysis system.
- Interact with the Huggingface App here: https://huggingface.co/spaces/mkbackup/YouTube

## How to run the code
Data Collection:

- Set up a Google API key for YouTube API access.
- Configure the .api_key file with YouTube API key and Hopsworks API key.
- Run the data collection code to gather comments from YouTube videos.
  
Model Training and Deployment:

- Configure the .api_key file with YouTube API key and Hopsworks API key.
- Train machine learning models using the provided code.
- Deploy models and vectorizer to Hopsworks Model Registry.
  
Gradio Interface:

- Configure the .api_key file with YouTube API key and Hopsworks API key.
- Run the Gradio interface code.
- Access the Gradio interface through the provided link, enter a YouTube video link, and analyze sentiment interactively.

## Conclusion
The YouTube Comment Sentiment Analysis project successfully demonstrates the end-to-end process of collecting data from YouTube, training machine learning models, deploying them on Hopsworks, and creating a user interface for sentiment analysis. The project provides valuable insights into audience sentiment for YouTube content creators and researchers interested in analyzing user feedback.
