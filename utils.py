import os,langchain
from langchain.globals import set_verbose
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
#from langchain_community.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI

def sql_agent(sql_uri,OPENAI_API_KEY):

    #llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0)
    db = SQLDatabase.from_uri(sql_uri)

    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(openai_api_key=OPENAI_API_KEY,temperature=0))
    agent_executor = create_sql_agent(
        llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0, model="gpt-3.5-turbo-0613"),
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )
    return agent_executor


def dataFrame_agent(df,OPENAI_API_KEY):

    agent_executor = create_pandas_dataframe_agent(
    ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    return agent_executor









