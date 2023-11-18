import streamlit as st 
from streamlit_chat import message as st_message
from dataclasses import dataclass
from typing import Literal


st.set_page_config(page_title="Log2Win!")

response = "blla blla"


with st.sidebar:
    st.title('Log2Win App')

    st.markdown('''
    ## About
    This app allows you to query different log files using natural language and get answers from a chatbot powered by our model.
    ''')

if "messages" not in st.session_state:
    st.session_state.messages=[]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Please give us a question regarding your log files")

if prompt:

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(   
        {"role":"user",
         "content":prompt})
    
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append(

            {
        "role":"assistant",
        "content":response
            }
        )