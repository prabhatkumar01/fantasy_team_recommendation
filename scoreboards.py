from google.cloud import storage, aiplatform
from google import genai
from google.genai import types
import base64
import io
import time


# Set up GCS client
# bucket_name = "ipl-scoreboards-2024"

def download_files_from_gcs(bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    files = {}

    for blob in blobs:
        file_content = blob.download_as_bytes()
        files[blob.name] = file_content.decode('utf-8')

    return files

def generate_prompt(files):
    prompt = "Here are the contents of the files:\n\n"
    for file_name, file_content in files.items():
        prompt += f"File: {file_name}\nContent:\n{file_content}\n\n"
    prompt += '''From the given match data, return the top 10 performing players in JSON format.
        {"top_players": ["Player1", "Player2", "Player3", ..., "Player10"]}'''
    
    return prompt

