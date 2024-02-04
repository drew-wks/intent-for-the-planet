import streamlit as st
from streamlit_extras.let_it_rain import rain
import utils
import os
import sys
import json
from data_models import Session, Responses
from st_files_connection import FilesConnection
import pandas as pd
from google.cloud import storage


url = st.secrets.QDRANT_URL_2

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

st.set_page_config(page_title="INTENT for the Planet", initial_sidebar_state="collapsed")

with open("config/custom_styles.css", "r", encoding='utf-8') as f:
    css_content = f.read()
st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)


import pandas as pd
from google.cloud import storage
from pydantic import BaseModel
import uuid
from typing import List


conn = st.connection('gcs', type=FilesConnection)
responses_df = conn.read("streamlit-data-bucket/intent/sessions.csv", input_format="csv", ttl=600)

st.dataframe(responses_df)