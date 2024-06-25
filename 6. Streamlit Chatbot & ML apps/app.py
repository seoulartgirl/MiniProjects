import streamlit as st
import openai
import os
from openai import OpenAI
st.title('식단 추천 Bot🤖')

openai.api_key = st.secrets['OPENAI_API_KEY']
client = OpenAI(api_key = os.getenv(openai.api_key))

if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

#initaialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

#React to user input
prompt = st.chat_input('내용을 입력하세요. 예: 단백질 위주의 식단 추천해줘')
if prompt:
    #Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    #add user message to chat history
    st.session_state.messages.append({'role':'user', 'content':prompt})

    with st.chat_message('assistant'):
        message_placeholder = st.empty() #empty placeholder
        full_response = ""
        #calling open api, stream=True for typing effect - interactive
        for response in client.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [{'role':m['role'], 'content':m['content']}
                        for m in st.session_state.messages], stream=True
        ):
            if response.choices[0].delta.content is not None:  # Check if the content is not None
                full_response += response.choices[0].delta.content
                message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({'role':'assistant','content':full_response})