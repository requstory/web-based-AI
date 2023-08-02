import streamlit as st
import os

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

st.title("👩🏿‍⚕️ Hi, I'm Doc")
st.write(
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)

with st.sidebar:
    "Example Search Items"
    "'What is the weather in my Lagos, Nigeria' today?'"
    "'Suggest birthday gifts for my wife, she likes running'"
    "'Who is the current Prime Minister of the United Kingdom?'"
    "'Who is the highest paid footballer in 2023?'"
    "'What new movies will be on Netflix this week?'"
    
    
    "[Write longer documents with Docuhelp.AI](https://docuhelp.ai)"
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content":  "...your AI assistant from Docuhelp. I will help you search the web so you dont have to..."}
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
         
        st.header(':mailbox: Get in touch with us!')
        
        contact_form = """
        <form action="https://formsubmit.co/9752bf2e61c2863896ec0aa20fe07e8a" method="POST">
             <input type="hidden" name="_captcha" value="false">
             <input type="email" name="email" placeholder='Your email' required>
             <button type="submit">Send</button>
        </form>
        """
        
        st.markdown(contact_form, unsafe_allow_html=True)
