from googleapiclient.discovery import build
from dotenv import dotenv_values

config = dotenv_values(".api_key")
key_value = config["KEY"]

print(key_value)