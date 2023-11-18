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

pos_answers = [
    "I found a log, that seems to fit your question:", 
    "I am happy to help, check out this log:",
    "I was checking out the file and found the following:",
    "Great news! I found a log that seems to fit your question. Here it is:",
    "I'm here to help! Check out what I found for you:",
    "Good news! While going through the files, I found the following log:",
    "I've been checking out the log files, and here's one that matches your query:",
    "Exciting! I found a log that should be helpful. Take a look:",
    "Happy to assist! Here's a log I came across that might interest you:",
    "The search is over! I found a log that aligns with your question. Check it out:",
    "Your timing is perfect! Here's a log I discovered that fits your inquiry:",
    "Success! I found a relevant log during my search. Take a look:",
    "I've got good news—I found a log that appears to address your question. Here it is:"
]

retry_pls = [
    "I'm sorry, but I'm having trouble understanding your question. Could you please rephrase or provide more details?",
    "Oops! It seems I didn't quite catch that. Can you try asking your question in a different way or providing additional information?",
    "I'm afraid I couldn't grasp the meaning of your question. Feel free to rephrase it, or let me know if you need assistance with something specific.",
    "I might have missed the mark on that one. Could you please clarify or ask your question in a different way?"
]

summary = None
uploaded_file = None
log_data = None

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

def get_summary(data):
    logSummarizer = LogSummarizer(log_data=data)
    summary = logSummarizer.summarize(5)
    return summary

if uploaded_file is not None:
    key, val = random.choice(list(jokes.items()))
    joke = (key + " " + val)
    with st.spinner(f'Processing Log File... Enjoy while you wait:\n{joke}'):  
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        log_data = stringio.read()
        summary = get_summary(log_data)
        logAIAgent = LogAIAgent()

    with st.chat_message("ai"):
        st.markdown("**Here is a summary of the logs:**")
        st.code(summary)
        st.markdown("**What do you want to know?**")

if 'details' not in st.session_state:
    st.session_state.details = ''

def set_details(line):
    st.session_state.details = logAIAgent.retrieve_log_snippet(line, log_data)

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
    if "?" in prompt:
        model_answer = logAIAgent.find_best_answer(summary,prompt)
        template = random.choice(pos_answers)
        formatted_answer =  logAIAgent.answer2summary(model_answer,summary)
        with st.chat_message("ai"):
            st.markdown(template)
            st.code(formatted_answer)
            st.markdown("Would you like to see the detailed logs?")
            st.button('Show Detailed Logs', on_click=set_details, args=(formatted_answer,))
        st.session_state.messages.append({"role": "ai", "content": formatted_answer})
    else:
        template = random.choice(retry_pls)
        with st.chat_message("ai"):
            st.markdown(template)
        st.session_state.messages.append({"role": "ai", "content": template})

st.session_state.details



