import streamlit as st
import utils
import os
from datetime import datetime
import sys
import pandas as pd
from pathlib import Path
import base64

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


st.set_page_config(page_title="INTENT for the Planet", initial_sidebar_state="collapsed")


st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True, )
hide_st_style = "<style>#MainMenu {visibility: hidden;}footer {visibility: visible;}header {visibility: visible;}</style>"
st.markdown(hide_st_style, unsafe_allow_html=True)
# Custom styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;500&display=swap');

        .logotype {
            font-family: Courier;
            color: #e06332;
        }

        .body {
            font-family: 'Lexend', sans-serif;
            font-weight: 300;
        }

        .header {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
        }

        /* Other styles */
        [data-testid="collapsedControl"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: visible; }
        header { visibility: visible; }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
    <style>
        .h3-style {
            font-size: 2.51em; /* Typical size of h3 */
            font-weight: bold; /* h3 is usually bold */
        }

        .h4-style {
            font-size: 2em; /* Typical size of h4 */
            font-weight: bold; /* h4 is usually bold */
        }
    </style>
    <span class="logotype h3-style">INTENT</span>
    <span class="header h4-style" style="color: #e06332;">® </span>
    <span class="header h4-style" style="color: black;">for the Planet</span>
""", unsafe_allow_html=True)


st.markdown('<p class="body">The intent of the session is to encourage introspection and personal growth, leading to a broader impact on the planet and its inhabitants.</p><br>', unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Contribute your INTENT", "Moderator's Guide", "Explore the INTENTs"])

with tab1:
    with st.form(key='planet_care_form'):
        user_responses = {
            "My world": st.text_area("1. What is your world?", placeholder="Just write down what comes to mind.", help="Reflect on what constitutes 'your world.' When you think of 'your world' what comes to mind? What is it that you can influence?").split('\\n'),
            "What the planet' is for me": st.text_area("2. What is 'the planet' for you?", placeholder="You can put more than one idea down.", help="Contemplate your relationship and connection to the planet.").split('\\n'),
            "How I care for my physical well-being": st.text_area("3. How do you care for your physical well-being?").split('\\n'),
            "How I care for my mental well-being": st.text_area("4. How do you care for your mental well-being?").split('\\n'),
            "My activities": st.text_area("5. What are your daily activities?").split('\\n'),
            "My resources": st.text_area("6. What are your resources?").split('\\n'),
            "Who I care about": st.text_area("7. Who do you care about?").split('\\n'),
            "How I cherish the planet": st.text_area("8. How do you cherish the planet and those who dwell here?").split('\\n'),
            "What I need to do more of": st.text_area("9. What do I need to do more of?").split('\\n'),
            "What I need to do less of": st.text_area("10. What do I need to do less of?").split('\\n'),
            "My Intent For the Planet": st.text_area("11. Your intent for the planet:").split('\\n')
        }
        submitted = st.form_submit_button("Submit")
        if submitted:
            utils.save_responses(user_responses)
            st.success("Thank you for your responses!")
            for key, values in user_responses.items():
                st.markdown(f"**{key}**:")
                for value in values:
                    st.markdown(f"*{value}*")


with tab2:
    doc = utils.read_markdown_file("moderation_guidance.md")
    st.markdown(doc, unsafe_allow_html=True)
    # st.markdown("This is a process to align our well-being with that of the planet:")


with tab3:
    st.markdown("Query the Repository", unsafe_allow_html=True)
    question = st.text_input("Ask a question:")
    synthetic = st.checkbox('Include synthetic data')
    response_file = "responses/responses_real.json" if not synthetic else "responses/responses_all.json"

    if st.button("Submit"):
        if question:
            response = utils.query(question, response_file)
            st.write(response)
        else:
            st.write("Please enter a question.")


st.markdown("""
<footer style="background: #f1f1f1; padding: 75px 5px 25px 15px;">
    <h5 class="logotype">INTENT<em>®</em></h5>
    <p class="body">Wesselsgade 15 B, st. th.<br />2200 København N<br />Denmark</p>
    <p class="logotype">INTENT<em>®</em><span class="body" style="color: #000000;"> is a trademark of <a href="http://www.intent.dk" title="INTENT">INTENT</a> CVR: 34944849</span></p>
</footer>
""", unsafe_allow_html=True)
