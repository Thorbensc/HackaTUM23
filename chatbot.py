import streamlit as st 
from streamlit_chat import message as st_message
from dataclasses import dataclass
from typing import Literal
from io import StringIO
from summarizer import LogSummarizer
from question_answering import LogAIAgent
import time
import random
st.set_page_config(page_title="Log2Win!")

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
upload_file = None

summary = None

def is_variable_initialized():
    return summary is not None

with st.sidebar:
    st.title('Log2Win App')

    st.markdown('''
    ## About
    This app allows you to query different log files using natural language and get answers from a chatbot powered by our model.
    ''')
    try:
        uploaded_file =  st.file_uploader(label="Upload your log file here")
    except:
        st.error("Could not parse Log File! Please try again ...")

if uploaded_file is not None:

    with st.spinner("Preparing Log File..."):
        try:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            log_data = stringio.read()

            logSummarizer = LogSummarizer(log_data=log_data[:10000])
            summary = logSummarizer.summarize(10)   
            while not is_variable_initialized():
                key, val = random.choice(list(jokes.items()))
                with st.chat_message("ai"):
                    joke = (key + ": " + val )
                    st.markdown(joke)
                    time.sleep(7)

            logAIAgent = LogAIAgent()

        except:
            st.error("Could not parse log data. Please provide a valid file.")

    with st.chat_message("ai"):
        answer = f'**Here is a summary of the logs:**\n\n{summary}\n**What do you want to know?**'
        st.markdown(answer)
    #st.session_state.messages.append({"role": "ai", "content": answer})

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# React to user input
if prompt := st.chat_input("Ask Questions about the Log File!"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    model_answer = logAIAgent.find_best_answer(summary,prompt)
    with st.chat_message("ai"):
        output_answer = [st.markdown(model_answer), st.markdown("Would you like to see the detailed logs?"), st.button("Show Detailed Logs")]
    st.session_state.messages.append({"role": "ai", "content": output_answer})
