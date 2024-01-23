# Interactive data inquiry

## Project Description: 
The project aims to develop a data retrieval system by seamlessly extracting information from both SQL databases and various file formats such as CSV and XLSX. To enhance user interaction, the system leverages the powerful OpenAI model from LangChain, integrating advanced natural language processing capabilities.

Use a ChatModel to retrieve relevant informations from a SQL database or csv,xlsx file.

1. Insert your OpenAI API key and upload a PDF file.
    - First method.
        Insert manually.
        <img width="1439"   src="./assets/interactive data inquiry ss1.png">
        
    - Second method to not insert the the OpenAI API key every session.
        1. Create a .env file and write your OpenAi key : 
            <img width="1400"   src="./assets/interactive data inquiry ss2.png">

        1. The folder will contain :
            
            ```
            .env
            utils.py
            interactive_data_inquiry.py
            ```
2. Choose if you want to interact with SQL database or csv, xlsx file.
    1. If csv or xlsx file upload the file.
    <img width="1400"   src="./assets/interactive data inquiry ss3.png">
    2. If SQL database choose MySQL or PostgreSQL and fill the parameters
    <img width="1400"   src="./assets/interactive data inquiry ss4.png">

3. Start Interacting.
    <img width="1400"   src="./assets/interactive data inquiry ss5.png">
## To Do's

- Add a prompt template for better and more accurate results, and to avoid errors resulting from a lack of context. .

