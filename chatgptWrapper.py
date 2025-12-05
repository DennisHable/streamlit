import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # načte env var z .env souboru

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # init; načte API klíč

st.set_page_config(page_title="ChatGPT Wrapper")
st.title("ChatGPT Wrapper")

if "messages" not in st.session_state: # historie konverzace
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
prompt = st.chat_input("Zadej zprávu...")

if prompt: # pokud uživatel něco napsal
    st.session_state.messages.append({"role": "user", "content": prompt}) # způsob ukládání historie konverzace
    with st.chat_message("user"): # pro uživatele vytvoří výstp
        st.write(prompt) # zápis
    with st.chat_message("assistant"): # odpoveď od AI
        stream_placeholder = st.empty() # nejdřív prázné pole
        streamed_text = ""
        stream = client.responses.create( # OpenAI api
            model="gpt-4o-mini", # typ modelu
            input=st.session_state.messages,
            stream=True, # výstup půjde postupně
        )
        for event in stream: 
            if event.type == "response.output_text.delta": # přišla další část dat - odpoveď od AI
                streamed_text += event.delta # append
                stream_placeholder.write(streamed_text) # zápis na stránku
            elif event.type == "response.completed": # po dokončení odpovědi se cyklus ukončí
                break
        st.session_state.messages.append(  # uložení odpovědi v rámci aktuální relace 
            {"role": "assistant", "content": streamed_text}
        )