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
        @import url('https://fonts.googleapis.com/css2?family=Lexend&display=swap');

        .logotype {
            font-family: Courier;
            color: #e06332;
        }

        .doc-style {
            font-family: 'Lexend', sans-serif;
        }

        .body {
            font-family: 'Lexend', sans-serif;
            font-weight: 300;
        }

        .sub-header {
            font-family: 'Lexend', sans-serif;
            font-weight: 400;
        }

        .header {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
        }
            
        /* Custom style to reduce vertical space */
        .markdown-text-container {
            margin-bottom: 5px !important;
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


st.markdown('<p class="sub-header">The intent of the session is to encourage introspection and personal growth, leading to a broader impact on the planet and its inhabitants.</p><br>', unsafe_allow_html=True)


tab1, tab2, tab3, tab4 = st.tabs(["About INTENT", "Contribute your INTENT", "Facilitator's Guide", "Explore the INTENTs"])

with tab1:
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    form_container = st.empty()
    with form_container:
        with st.form(key='intent_responses'):
            user_responses = {
                "My world": st.text_area("1. What is your world?", placeholder="Reflect on what constitutes 'your world.' Just write down what comes to mind.", help="When you think of 'your world' what comes to mind? What is it that you can influence?").split('\\n'),
                "What the planet' is for me": st.text_area("2. What is 'the planet' for you?", placeholder="You can put more than one idea down.", help="Contemplate your relationship and connection to the planet.").split('\\n'),
                "How I care for my physical well-being": st.text_area("3. How do you care for your physical well-being?",placeholder="You can put more than one idea down.", help="Reflect on the things you do to support your physical well-being.").split('\\n'),
                "How I care for my mental well-being": st.text_area("4. How do you care for your mental well-being?",placeholder="Similar to above.", help="Think about activities and practices that contribute to your mental health. What are the things you do that give you mental peace?").split('\\n'),
                "My activities": st.text_area("5. What are your daily activities?",placeholder="List your daily activities. What do you do?", help="For the moment, don't be concerned avout how these may or may not affect the planet. Just simply-- what are your activities? How do you spend your time?").split('\\n'),
                "My resources": st.text_area("6. What are your resources?",placeholder="Write a list of your resources.", help="These may be inner or outer resources What do you have that you can use?").split('\\n'),
                "Who I care about": st.text_area("7. Who do you care about?",placeholder="Note these down as they come to you.", help="Reflect on the people and relationships that are important to you.").split('\\n'),
                "How I cherish the planet": st.text_area("8. How do you cherish the planet and those who dwell here?",placeholder="You can put more than one idea down.", help="What do you currently do to cherish the planet and those who dwell here? You can also include things you are planning to do soon.").split('\\n'),
                "What I need to do more of": st.text_area("9. What do I need to do more of?",placeholder="You can put more than one idea down.", help="Reflecting a little on what you have written above, what would you like to do more of?").split('\\n'),
                "What I need to do less of": st.text_area("10. What do I need to do less of?",placeholder="You can put more than one idea down.", help="Reflecting on your life at the moment, what would benefit you to do less of?").split('\\n'),
                "My Intent For the Planet": st.text_area("11. Your intent for the planet:",placeholder="This is a creative process. Don't think too hard about it. Just write down whatever comes to mind.", help="Use the insights from the session to draft a statement of intent for the planet, rreflecting on your personal values, goals, and the ways you wish to contribute positively. Use the individual template 'INTENT for the planet' as a kind of guide for your own personal vision").split('\\n')
            }
            submitted = st.form_submit_button("Submit", type="primary")
        if submitted:
            #utils.save_responses(user_responses)
            st.session_state['user_responses'] = user_responses
            form_container.empty()
    if submitted:
        st.success("Thank you for contributing your Intent for the planet!")
        st.balloons()
        file_content = ""
        for key, values in st.session_state['user_responses'].items():
            st.markdown(f"**{key}**:")
            file_content += f"{key}:\n"  # Add key to the file content
            for value in values:
                st.markdown(f"*{value}*")
                file_content += f"- {value}\n"  # Add value to the file content
            file_content += "\n"  # Add a newline for spacing between sections

        # Create a download button
        st.download_button(
            label="Download Responses as Text",
            data=file_content,
            file_name=f"my_IFTP_{utils.now_utc}.txt",
            mime="text/plain"
        )


with tab3:
    doc = utils.read_markdown_file("facilitation_guide.md")
    st.markdown(doc, unsafe_allow_html=True)


with tab4:
    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sub-header markdown-text-container">Ask a question of the collection of INTENTs:</span>', unsafe_allow_html=True)
    question = st.text_input("", placeholder="Type your question here")
    synthetic = st.toggle('Include synthetic data')
    response_file = "responses/responses_real.json" if not synthetic else "responses/responses_all.json"

    if st.button("Submit", type="primary"):
        if question:
            response = utils.query(question, response_file)
            st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True) 
            st.markdown(f'<p class="header">Response:</p><div class="body">{response}</div>', unsafe_allow_html=True)

        else:
            st.write("Please enter a question.")
    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)


st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
st.markdown("""
<footer style="background: #f1f1f1; padding: 60px 5px 25px 20px;">
    <h5 class="logotype">INTENT<em>®</em></h5>
    <p class="body">Wesselsgade 15 B, st. th.<br />2200 København N<br />Denmark</p>
    <p class="logotype">INTENT<em>®</em><span class="body" style="color: #000000;"> is a trademark of <a href="http://www.intent.dk" title="INTENT">INTENT</a> CVR: 34944849</span></p>
    <p class="body">ai by <a href="http://www.wks.us" title="wks" class="header" style="color: #D70E10; text-decoration: none;">wks</a></p>
</footer>
""", unsafe_allow_html=True)
