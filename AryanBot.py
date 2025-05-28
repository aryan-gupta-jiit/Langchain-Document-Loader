from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

load_dotenv()
url="https://github.com/aryan-gupta-jiit"
web_loader=WebBaseLoader(url)

web_info=web_loader.load()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content='You are a helpful AI assistant')
    ]

model=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

prompt=PromptTemplate(
        template='Read the {Resume} and {webPage} thoroughly and answer the following {query}',
        input_variables=["Resume","webPage","query"],
    )

loader=PyPDFLoader('Aryan_Gupta_resume_latest.pdf')

docs=loader.load()

parser=StrOutputParser()

chain=prompt|model|parser

# streamlit UI
st.title("Talk to Virtual Aryan 🤖")
st.caption("Ask questions about him")

# while True:
#     user_query = input("Write your query here: ")
#     chat_history.append(HumanMessage(content=user_query))

#     if user_query.lower()=='exit':
#         break

#     res=chain.invoke({'Resume':docs[0].page_content,'query':user_query})

#     chat_history.append(AIMessage(content=res))
#     print('AI:',res)

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

user_query = st.chat_input("Ask questions : ")

if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("user"):
        st.write(user_query)

    with st.spinner("Thinking..."):
        res=chain.invoke({'Resume':docs[0].page_content,'webPage':web_info,'query':user_query})

    st.session_state.chat_history.append(AIMessage(content=res))

    with st.chat_message("assistant"):
        st.write(res)





