import streamlit as st 
from streamlit_chat import message as st_message
from dataclasses import dataclass
from typing import Literal
from io import StringIO
from summarizer import LogSummarizer
from question_answering import LogAIAgent

st.set_page_config(page_title="Log2Win!")

response = "blla blla"
summary = ""
upload_file = None

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.title('Log2Win App')

    st.markdown('''
    ## About
    This app allows you to query different log files using natural language and get answers from a chatbot powered by our model.
    ''')
    
    uploaded_file =  st.file_uploader(label="Upload your log file here")

if uploaded_file is not None:

    with st.status("Summarizing data..."):
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        log_data = stringio.read()

        logSummarizer = LogSummarizer(log_data=log_data[:3000])
        summary = logSummarizer.summarize(10)   

        logAIAgent = LogAIAgent()

    st.text(summary)
        

prompt = st.chat_input("Please give us a question regarding your log files")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    model_answer = logAIAgent.find_best_answer(summary,prompt)
    with st.chat_message("ai"):
        st.markdown(model_answer)