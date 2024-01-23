import streamlit as st
import base64
import os
from langchain_community.callbacks import get_openai_callback # Check number of token use per request
import openai
from dotenv import load_dotenv
import requests
from utils import sql_agent,dataFrame_agent
import pathlib
import pandas as pd


def check_openai_api_key(api_key):
    if api_key =='':
        return False
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

#clear chat history
def on_btn_click():
    del st.session_state.messages[:]
    


if "tokens" not in st.session_state:
    st.session_state['tokens'] = []

if "cost" not in st.session_state:
    st.session_state['cost'] = []



if __name__ == '__main__':
    with st.sidebar:
        st.title("Interactive data inquiry")

    #Check if there is a given key in the .env file and if it's a valid one
    load_dotenv()
    get_key = os.getenv('OPENAI_API_KEY')
    
    if get_key : 

        OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        if not check_openai_api_key(OPENAI_API_KEY):
            with st.sidebar:
                st.write("Please insert a valid key")
    else:
        with st.sidebar:
            OPENAI_API_KEY = st.text_input("OPENAI API KEY",type="password")


    with st.sidebar:
        
        #Check if given key is valid
        try:
            if not check_openai_api_key(OPENAI_API_KEY):
                OPENAI_API_KEY = st.text_input("OPENAI API KEY",type="password")
                
            else : 
                st.write("Valid key")
        except:
            with st.sidebar:
                st.write("Please insert a valid key")
            
    connected = False
    
    with st.sidebar:
        database = st.radio(
    "Select csv file or  SQL database",
    ["CSV or XLSX", "SQL database"],
    index=None
    )
        
        if database == 'SQL database' and check_openai_api_key(OPENAI_API_KEY):
            sql = st.radio(
                "Select one of the following : ",
                ['MySQL','PostgreSQL'],
                index= None
            )
            if sql is not None :
                with st.form('my form'):
                    with st.sidebar:
                        #Comments this part and uncomments the part below with the right setting to not submit the parameters for the same database during each session 
                        user = st.text_input("User") 
                        password = st.text_input("Password",type='password')
                        host = 'localhost' # st.text_input("Host")
                        port = st.text_input("Port")
                        sql_database = st.text_input('Database name')
                        submitted = st.form_submit_button('Submit')

                        #user=''
                        #password=''
                        #host=''
                        #port = ''
                        #sql_database=''

                if sql =="MySQL":
                    sql_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{sql_database}"

                elif sql =='PostgreSQL':
                    sql_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{sql_database}" 

                if check_openai_api_key(OPENAI_API_KEY) and user !='' and password !='' and host !='' and port !='' and sql_database !='':
                    try :
                        agent = sql_agent(sql_uri,OPENAI_API_KEY=OPENAI_API_KEY)
                        connected = True
                        with st.sidebar:
                            st.write('Connected to database successfully')
                    except:
                        with st.sidebar:
                            st.write("Could not connect to database")

        elif database == "CSV or XLSX" and check_openai_api_key(OPENAI_API_KEY):
            uploaded_file = st.file_uploader("Upload a csv or xlsx or file",type=["csv","xlsx"],help="Only csv or xlsx files are supported")
        
            if uploaded_file is not None:
                if pathlib.Path(uploaded_file.name).suffix == '.csv':
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                try :
                    agent = dataFrame_agent(df,OPENAI_API_KEY=OPENAI_API_KEY)
                    connected = True
                    
                    with st.sidebar:
                        st.write('File imported successfully and ready to chat')
                except:
                    with st.sidebar:
                        st.write("Could not process the file")
        
    if database is not None and connected :                     
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if prompt !='':
                with get_openai_callback() as cb : 
                    answer = agent.run(prompt)

            st.session_state.tokens.append(cb.total_tokens)
            st.session_state.cost.append(cb.total_cost)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                message_placeholder.markdown(answer)
    
                st.write("Tokens used : ",cb.total_tokens)
                st.write("Prompt tokens : ",cb.prompt_tokens," | ","Completions tokens : ",cb.completion_tokens)
                st.session_state.messages.append({'role':"assistent", "content": answer})

        with st.sidebar:
            st.button("Clear history", on_click=on_btn_click)

    with st.sidebar:
        st.subheader("Tokens and cost tracking",divider="rainbow")
        st.write("Total tokens used : ",sum(st.session_state.tokens))
        st.write(f'Cost : {sum(st.session_state.cost)} $')
        