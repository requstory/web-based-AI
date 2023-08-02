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
         
    formbtn = st.button("Like this?")
    if "formbtn_state" not in st.session_state:
        st.session_state.formbtn_state = False
        
    if formbtn or st.session_state.formbtn_state:
        st.session_state.formbtn_state = True
            
        st.subheader("Contact us")
        # name = st.text_input("Name")
        with st.form(key = 'user_info'):
            st.write('Like this? Lets get you one')
            
            name = st.text_input(label="Name 📛")
            email = st.text_input(label="Email 📧")
            phone = st.text_input(label="Phone 📱")
            
            submit_form = st.form_submit_button(label="Subscribe", help="Click to subscribe!")
            
                # Checking if all the fields are non empty
            if submit_form:
                st.write(submit_form)
            
                if name and email :
                        # add_user_info(id, name, age, email, phone, gender)
                    st.success(f"ID:  \n Name: {name} \n Email: {email}"
                                )
                    else:
                        st.warning("Please fill all the fields")
        
