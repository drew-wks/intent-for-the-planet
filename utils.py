import streamlit as st
import json
import io
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
import uuid
from uuid import UUID
from qdrant_client import QdrantClient, models 
import openai
from pathlib import Path
import pandas as pd
from st_files_connection import FilesConnection
import logging
from google.cloud import storage
import pandas as pd
import ast


api_key = st.secrets["QDRANT_API_KEY_2"]
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = QdrantClient("https://1be15a39-6a90-4270-b4fe-09cdf7a01d22.us-east4-0.gcp.cloud.qdrant.io",
                    prefer_grpc=True,
                    api_key=api_key,
                    )


now_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")



def read_markdown_file(markdown_file):
    """read in a markdown file for display in streamlit"""
    return Path(markdown_file).read_text()



# Custom JSON encoder that converts UUIDs to strings
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)



def append_to_gcs_file(data_object, gcs_file_name):
    '''Example usage
    append_to_gcs_file(session, 'sessions.csv')
    '''
    data_object_dict = data_object.dict(by_alias=True)
    df = pd.json_normalize(data_object_dict, sep='_')
    storage_client = storage.Client.from_service_account_info(st.secrets["gcs_connections"])
    bucket = storage_client.get_bucket('streamlit-data-bucket')
    blob = bucket.blob('intent/' + gcs_file_name)
    blob_data = blob.download_as_text()
    existing_df = pd.read_csv(io.StringIO(blob_data))
    updated_df = pd.concat([existing_df, df], ignore_index=True)
    updated_csv = updated_df.to_csv(index=False)
    blob.upload_from_string(updated_csv, content_type='text/csv')



def dict_to_markdown(dict):
    """
    Takes a dictionary of responses and formats it into a Markdown string.
    
    Args:
    - responses_dict: A dictionary where keys are questions and values are responses.
    
    Returns:
    - A string formatted in Markdown.
    """
    now_date = datetime.now()
    formatted_date = now_date.strftime("%A, %B %d, %Y")
    
    markdown_str = "### My INTENT for the Planet\n  "
    markdown_str += f"{formatted_date}\n\n<br>"
    for question, response in dict.items():
        # Split responses into lines for multi-line responses
        formatted_response = response.replace("\n", "<br>")
        # Append the question and formatted response to the Markdown string
        markdown_str += f"**{question}**<br>{formatted_response}\n\n"
    
    return markdown_str

# Example usage with your dictionary
responses_dict = {
    '1. What is your world?': 'A place of unity and respect',
    "2. What is 'the planet' is for you?": 'A shared home for all beings',
    '3. How do you care for your physical well-being?': 'Regular exercise\nHealthy eating',
    '4. How do you care for your mental well-being?': 'Meditation\nReading',
    '5. What are your activities?': 'Public speaking\nWriting\n',
    '6. What are your resources?': 'My books\nCommunity support',
    '7. Who do you care about?': 'Family\nNation\n',
    '8. How do you cherish the planet?': 'Promoting sustainability\neducating others\n',
    '9. What do you need to do more of?': 'Listening to diverse perspectives\n\n',
    '10. What do you need to do less of?': 'Spending time on trivial matters\nNeglecting self-care',
    'My Intent For the Planet': 'To foster a world of equality and understanding\nTo provide food for us all\nTo have an educated and caring world'
}



def clean_df_list_columns(df):
    """
    Cleans columns in the DataFrame that contain string representations of lists,
    converting them to a string with items separated by newline characters.
    """
    def clean_list_field(list_str):
        try:
            actual_list = ast.literal_eval(list_str)
            if isinstance(actual_list, list):
                return '\n'.join(actual_list)
            else:
                return list_str
        except (ValueError, SyntaxError):
            return list_str

    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: clean_list_field(x) if pd.notnull(x) else x)

    return df



def pd_row_navigation(df):
    """
    Sets up navigation for viewing DataFrame rows one at a time in Streamlit.
    
    Returns:
    - A tuple of functions (next_row, prev_row) for navigating the DataFrame rows.
    """
    if 'current_row_index' not in st.session_state:
        st.session_state['current_row_index'] = len(df) - 1  # Start from the last row

    def next_row():
        # Decrement the index to move to the previous row in natural order, which is "next" in reverse
        if st.session_state['current_row_index'] > 0:
            st.session_state['current_row_index'] -= 1

    def prev_row():
        # Increment the index to move to the next row in natural order, which is "previous" in reverse
        if st.session_state['current_row_index'] < len(df) - 1:
            st.session_state['current_row_index'] += 1

    return next_row, prev_row



def query(question, response_file):
    """read in the json file as source data for the QA (this is temporary as we're building)"""
    with open(response_file, encoding='utf-8') as f:
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
