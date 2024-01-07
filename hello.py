import streamlit as st
import json
import os
from datetime import datetime
import uuid
import openai


st.set_page_config(page_title="INTENT for the Planet", initial_sidebar_state="collapsed")

st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True, )


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: visible;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                }
        </style>
        """, unsafe_allow_html=True)


# Function to save responses to a JSON file matching the given schema
def save_responses(responses_content):
    # Define the filename
    filename = "responses/responses.json"
    
    # Create a response dictionary matching the schema
    response = {
        "id": str(uuid.uuid4()),
        "metadata": {
            "p_num": "",
            "p_haplotype": "",
            "p_id": "",
            "schema": "1",
            "version": "1",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "response": responses
    }
    
    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, load the existing data and append the new response
        with open(filename, 'r') as file:
            data = json.load(file)
        data.append(response)
    else:
        # If the file does not exist, create a new list with the response
        data = [response]
    
    # Save the data to a JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


st.title("INTENT for the Planet")

st.markdown(f"The intent of the session is to encourage introspection and personal growth, leading to a broader impact on the planet and its inhabitants.")

tab1, tab2, tab3 = st.tabs(["Contribute your Intent", "Moderator's Guide", "Explore the Intents"])

with tab1:
    with st.form(key='planet_care_form'):
        responses = {
            "My world": st.text_area("1. What is your world?", placeholder="Just write down what comes to mind.", help="Reflect on what constitutes 'your world.' When you think of 'your world' what comes to mind? What is it that you can influence?"),
            "What the planet' is for me": st.text_area("2. What is 'the planet' for you?", placeholder="You can put more than one idea down.", help="Contemplate your relationship and connection to the planet."),
            "How I care for my physical well-being": st.text_area("3. How do you care for your physical well-being?").split('\\n'),
            "How I care for my mental well-being": st.text_area("4. How do you care for your mental well-being?").split('\\n'),
            "My activities": st.text_area("5. What are your daily activities?").split('\\n'),
            "My resources": st.text_area("6. What are your resources?").split('\\n'),
            "Who I care about": st.text_area("7. Who do you care about?").split('\\n'),
            "How I cherish the planet": st.text_area("8. How do you cherish the planet?").split('\\n'),
            "What I need to do more of": st.text_area("9. What do I need to do more of?").split('\\n'),
            "What I need to do less of": st.text_area("10. What do I need to do less of?").split('\\n'),
            "My Intent For the Planet": st.text_area("11. Your intent for the planet:").split('\\n')
        }

        submitted = st.form_submit_button("Submit")
        if submitted:
            save_responses(submitted)
            st.success("Thank you for your responses!")
            st.markdown(submitted)

    with tab2:
        st.markdown("Moderator's Guide", unsafe_allow_html=True)
        doc = read_markdown_file("moderation_guidance.md")
        st.markdown(doc, unsafe_allow_html=True)
        # st.markdown("This is a process to align our well-being with that of the planet:")
    
    with tab3:
        st.markdown("Query the Repository", unsafe_allow_html=True)
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        def query(question):
            with open(response_file) as f:
                data = json.load(f)


            messages =  [  
                {'role':'system', 
                'content': "You are a helpful assistant. Try to answer the users question based on the info in the json provided"},    
                {'role':'user', 
                'content': f"""{question}```{data}```"""}  
            ] 

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k", 
                messages=messages,
                temperature=0, 
                max_tokens=8000,
            )
            return response.choices[0].message["content"]
        

        question = st.text_input("Ask a question:")
        synthetic = st.checkbox('Include synthetic data')
        response_file = "responses/responses_real.json" if not synthetic else "responses/responses_all.json"

        if st.button("Submit"):
            if question:
                # Call the query function with the user's question
                response = query(question)
                st.write(response)
            else:
                st.write("Please enter a question.")