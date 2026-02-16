import streamlit as st
from openai import OpenAI
from datetime import datetime
import json
import os

API_URL = ("https://api.xxxxxx.com/v1") # Input ur API URL here (dont forget to put /v1 at the end)
API_KEY = ("sk-xxxxxxxxxxxxx") # Input ur API KEY here
MODEL_NAME = ("MODEL_NAME") # Select ur model here (still the same, use /v1/models to look it up)

client = OpenAI(base_url=API_URL, api_key=API_KEY)

st.set_page_config(page_title="SimpleChatbot", page_icon="👾")
st.title("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Actions")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💾 Save Chat"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"chat_{timestamp}.json"
        with open(filename, "w") as save:
            json.dump(st.session_state.messages, save)
        st.success(f"Saved: {filename} !")
    
    st.divider()
    
    chat_files = [f for f in os.listdir() if f.startswith("chat_") and f.endswith(".json")]
    chat_files.sort(reverse=True)
    
    if chat_files:
        st.subheader("📂 Load Chat")
        selected = st.selectbox("Select chat:", chat_files)
        
        if st.button("Load"):
            with open(selected, "r") as loadz:
                st.session_state.messages = json.load(loadz)
            st.success(f"Locked and Loaded! : {selected}")
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Input Your Message Here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=st.session_state.messages
                )
                ai_msg = response.choices[0].message.content
                st.write(ai_msg) #output
                
                st.session_state.messages.append({"role": "assistant", "content": ai_msg}) #add to history
            
            except Exception as e:
                st.error(f"Error: {e}") #error handling