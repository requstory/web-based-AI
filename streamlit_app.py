import streamlit as st
import os

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

st.title("👩🏿‍⚕️ Hi, I'm Doc from Docuhelp")
st.write(
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)

with st.sidebar:
    "Example Search Items"
    "What is the weather in my City today?"
    "Suggest birthday gifts for my wife, she likes running"
    "Who is the Prime Minister of the United Kingdom"
    "[Write longer documents with Docuhelp.AI](https://docuhelp.ai)"


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content":  "I'm your AI Assistant. Let me help you with your search"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


    llm = ChatOpenAI(model_name="gpt-3.5-turbo", streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
