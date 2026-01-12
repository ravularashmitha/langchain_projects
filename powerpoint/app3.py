import streamlit as st 
import requests 

st.title("chatbot")
if "conversation" not in st.session_state:
    st.session_state["conversation"]=[]
    

    

prompt=st.chat_input("type the message")

if prompt:
      st.session_state["conversation"].append({"role":"user","data":prompt})
    
      response=requests.post(url="https://alexa07.app.n8n.cloud/webhook-test/0bf712de-d9fa-470f-b96a-d00637403ef7",json={"prompt":prompt})
    
    
    
      if response.status_code==200:
        st.session_state["conversation"].append({"role":"ai","data":response.json()["output"]})

    
for c in  st.session_state["conversation"]:
    
    with st.chat_message(c["role"]):
        st.write(c["data"])
      