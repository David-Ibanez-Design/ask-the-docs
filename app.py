# Import necessary libraries and modules
import streamlit as st
import tempfile
import pandas as pd
from src.chat import handleChat
import os
from dotenv import load_dotenv
from src.assets.styles import css
from codeinterpreterapi import File

load_dotenv()

# Open AI API Key
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')

# Page layout
st.set_page_config(page_title='Ask the Doc App')
st.title('Ask the Doc App')

# Load CSS
st.write(css,unsafe_allow_html=True)

holder = st.empty()

with holder.container():

    # API key form
    st.subheader('1. Enter your OpenAI API key')
    input_api_key = st.text_input('OpenAI API key', type='password', key='api_key', value=OPEN_AI_KEY)

    # File upload form
    st.subheader('2. Upload or select your a CSV or xlsx file')
    uploaded_file = st.file_uploader("Upload a file", key="uploaded_file")


if len(input_api_key) > 0 and uploaded_file is not None:
    holder.empty()

    # Upload file
    uploaded_files_list = []
    bytes_data = uploaded_file.read()
    uploaded_files_list.append(File(name=uploaded_file.name, content=bytes_data))

    # Get file path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    filename, file_extension = os.path.splitext(uploaded_file.name)

    if file_extension == '.csv':
        df = pd.read_csv(tmp_file_path)
    if file_extension == '.xlsx':
        df = pd.read_excel(tmp_file_path)

    # Displayed uploaded document
    with st.sidebar:
        st.title(uploaded_file.name + ' preview')
        st.dataframe(df,height= 500)

    handleChat(filename, df.columns, uploaded_files_list)
