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

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


# Function to save responses to a JSON file matching the given schema
def save_responses(responses_content):
    # Define the filename
    filename = "responses/responses.json"
    
    # Create a response dictionary matching the schema
    response = {
        "id": str(uuid.uuid4()),
        "metadata": {
            "p_num": "",
            "p_haplotype": "",
            "p_id": "",
            "schema": "1",
            "version": "1",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "response": responses
    }
    
    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, load the existing data and append the new response
        with open(filename, 'r') as file:
            data = json.load(file)
        data.append(response)
    else:
        data = [response]
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()


openai.api_key = st.secrets["OPENAI_API_KEY"]

def query(question):
    with open(response_file) as f:
        data = json.load(f)


    messages =  [  
        {'role':'system', 
        'content': "You are a helpful assistant. Try to answer the users question based on the info in the json provided"},    
        {'role':'user', 
        'content': f"""{question}```{data}```"""}  
    ] 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", 
        messages=messages,
        temperature=0, 
        max_tokens=8000,
    )
    return response.choices[0].message["content"]
