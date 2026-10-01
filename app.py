
import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    
)
st.title("AI Chatbot")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
)


# System prompt

system_message = SystemMessage(content="""You are a helpful AI assistant.
                              Give clear and simple answers.
                              if the user asks a technical question, explain it with an example.""")

# Chat History

if "messages" not in st.session_state:
    st.session_state.messages = [system_message]
    
# Sidebar

with st.sidebar:
   st.header("Settings")
   
   if st.button("Clear Chat"):
       st.session_state.message = [system_message]
       st.rerun()
        
# Display Chat

for message in st.session_state.messages:
   if isinstance(message, HumanMessage):
           with st.chat_message("user"):
                st.write(message.content)
   elif isinstance(message,AIMessage):
       with st.chat_message("assistant"):
           st.write(message.content) 
                
# User Input
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        st.session_state.messages.append(HumanMessage(content=user_input))
        
        try:
            # Get AI response
            response = llm.invoke(st.session_state.messages)
            
            # Add AI message
            st.session_state.messages.append(AIMessage(content=response.content))
            with st.chat_message("assistant"):
                st.write(response.content)
        except Exception as e:
            st.error(f"Error: {e}")           
        
            