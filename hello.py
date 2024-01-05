import streamlit as st
import json
import os
from datetime import datetime
import uuid

# Function to save responses to a JSON file matching the given schema
def save_responses(responses_content):
    # Define the filename
    filename = "responses.json"
    
    # Create a response dictionary matching the schema
    response = {
        "response_id": str(uuid.uuid4()),
        "participant_id": str(uuid.uuid4()),
        "response_version": "1",
        "response_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "response_content": responses_content
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

# Title of the app
st.title("Reflections for a Better Planet")

# Streamlit form to collect responses
with st.form(key='planet_care_form'):
    st.subheader("Please answer the following questions:")
    responses_content = {
        "My world": st.text_input("1. What is your world?"),
        "What 'the planet' is for me": st.text_input("2. What is 'the planet' for you?"),
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

    # Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        save_responses(responses_content)
        st.success("Thank you for your responses!")

# Inform the user where the responses will be saved
st.info("Your responses will be saved to a JSON file in the server.")
