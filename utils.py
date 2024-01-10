import streamlit as st
import json
import os
from datetime import datetime
import uuid
import openai
import sys
import pandas as pd
from pathlib import Path
import os
import base64


responses_dir = "responses_test"
now_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
filename = os.path.join(responses_dir, f"response_{now_utc}.json")

# Function to save responses to a JSON file matching the given schema
def save_responses(responses):
    # Define the filename
    filename = f"responses/response_{now_utc}.json"
    
    # Create a response dictionary matching the schema
    entity = {
        "id": str(uuid.uuid4()),
        "metadata": {
            "p_num": "",
            "p_haplotype": "",
            "p_id": "",
            "schema": "1",
            "version": "1",
            "date": now_utc,
        },
        "response": responses
    }
    
   # Check if the responses directory exists; if not, create it
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)
    
    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, load the existing data and append the new response
        with open(filename, 'r') as file:
            data = json.load(file)
        data.append(entity)
    else:
        data = [entity]
    
    # Save the data to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)



def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()


openai.api_key = st.secrets["OPENAI_API_KEY"]

def query(question, response_file):
    with open(response_file) as f:
        data = json.load(f)


    messages =  [  
        {'role':'system', 
        'content': "You are a helpful assistant. Try to answer the users question based on the info in the INTENTs provided. You can supplement your response with your own information, but if you do please let user know what information you added. If you don't know the answer to something, just say I don't know."},    
        {'role':'user', 
        'content': f"""{question}```{data}```"""}  
    ] 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  #gpt-4
        messages=messages,
        temperature=0.8, # 0-2. Controls response randomness vs determinism. Higher is more random 
        max_tokens=8000,
    )
    return response.choices[0].message["content"]
