import streamlit as st
import requests

from langchain import OpenAI
from langchain.agents import initialize_agent, load_tools, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import DuckDuckGoSearchRun

# Set the title of the Streamlit app
st.title('Web based AI Search')
st.write(
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)

llm = OpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.8,
    model_name="text-davinci-003"
)

prompt = PromptTemplate(
  input_variables=["query"],
  template="You are New Native Internal Bot. Help users with their important tasks, like a professor in a particular field. Query: {query}"
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

search = DuckDuckGoSearchRun()

# Web Search Tool
search_tool = Tool(
    name = "Web Search",
    func=search.run,
    description="A useful tool for searching the Internet to find information on world events, issues, etc. Worth using for general topics. Use precise questions."
)

agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=[search_tool],
    llm=llm,
    verbose=True, # I will use verbose=True to check process of choosing tool by Agent
    max_iterations=3
)

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  
r_1 = st.text_input
r_1 = agent("Who is the President of Brazil?")
print(f"Final answer: {r_1['output']}")
