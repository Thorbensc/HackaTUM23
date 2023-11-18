import streamlit as st 
from streamlit_chat import message as st_message
from dataclasses import dataclass
from typing import Literal
from io import StringIO
from summarizer import LogSummarizer
from question_answering import LogAIAgent
import time
import random

jokes = {"Why don't scientists trust atoms?":'Because they make up everything!', 
         'What did one wall say to the other wall?':"I'll meet you at the corner",
         "Why did the bicycle fall over?":"Because it was two-tired!",
         "How does a penguin build its house?":"Igloos it together!",
         "What do you call fake spaghetti?":"An impasta!",
         "Why did the scarecrow win an award?":"Because he was outstanding in his field!",
         "Did you hear about the mathematician who's afraid of negative numbers?":"He'll stop at nothing to avoid them!",
         "What do you get when you cross a snowman and a vampire?":"Frostbite!",
         "Why did the tomato turn red?":"Because it saw the salad dressing!",
         "How do you organize a space party?":"You planet!"
         }
summary = ""
uploaded_file = None

st.set_page_config(page_title="logai by Log2Win")
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #your_color_code_here;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #eaf2ef;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logo_image = "Logo_vertikal.svg"
    st.sidebar.image(logo_image, width=300)
    st.markdown('''
    ## About Me
    I give your log files a voice. As an interactive assistant I allow you to gather insightful information by asking simple questions.
    ''')

    try:
        uploaded_file =  st.file_uploader(label="Upload your log file here")
    except:
        st.error("Could not parse Log File! Please try again ...")

def get_summary(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    log_data = stringio.read()

    logSummarizer = LogSummarizer(log_data=log_data[:3000])
    summary = logSummarizer.summarize(10)
    return summary

if uploaded_file is not None:
    key, val = random.choice(list(jokes.items()))
    joke = (key + " " + val)
    with st.spinner(f'Preparing Log File...\n{joke}'):  
        summary = get_summary(uploaded_file)
        logAIAgent = LogAIAgent()

    with st.chat_message("ai"):
        st.markdown("**Here is a summary of the logs:**")
        st.code(summary)
        st.markdown("**What do you want to know?**")

if 'details' not in st.session_state:
    st.session_state.details = ''

def set_details():
    st.session_state.details = "DETAILS!!!!!"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Questions about the Log File!"):
    st.session_state.details = ''
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    model_answer = logAIAgent.find_best_answer(summary,prompt)

    with st.chat_message("ai"):
        st.markdown(model_answer)
        st.markdown("Would you like to see the detailed logs?")
        st.button('Show Detailed Logs', on_click=set_details)
    st.session_state.messages.append({"role": "ai", "content": model_answer})

st.session_state.details



