import datetime
import streamlit as st
import sys
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path
import os
import base64

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

st.set_page_config(page_title="Intent for the Planet", initial_sidebar_state="collapsed")

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



def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()



st.title("INTENT for the Planet", use_column_width="always")
st.markdown(f"The intent of the session is to encourage introspection and personal growth, leading to a broader impact on the planet and its inhabitants.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contribute your Intent", "Query the Repository", "Moderator's Guide"])

with tab1:
    overview = read_markdown_file("pages/ask_overview.md")
    st.markdown(overview, unsafe_allow_html=True)
    

with tab2:
    df, last_update_date = ASK.get_library_list_excel_and_date()
    overview = read_markdown_file("pages/library_overview.md")

    if df is not None:
        num_items = len(df)
        st.markdown("#### Library Overview")
        st.markdown(f"ASK is loaded with **{num_items}** national documents (almost 9000 pages) including USCG Directives, CHDIRAUX documents and documents issued by the USCG Auxiliary National leadership. All these documents are located in public sections of the USCG and USCG Auxiliary websites (cgaux.org uscg.mil).  No secure content is included (i.e., content requiring Member Zone or CAC access. All documents are national. Regional requirements may vary, so check with your local AOR leadership for the final word. ")
        st.markdown(f"{overview}")
        st.markdown("#### Document List")
        st.markdown(f"{num_items} items. Last update: {last_update_date}")  

        # Display the DataFrame
        display_df = df[['source_short']]
        edited_df = st.data_editor(display_df, use_container_width=True, hide_index=False, disabled=True)
        isim = 'ASK_library.csv'
        indir = edited_df.to_csv(index=False)
        b64 = base64.b64encode(indir.encode(encoding='ISO-8859-1')).decode(encoding='ISO-8859-1')  
        linko_final = f'<a href="data:file/csv;base64,{b64}" download={isim}>Click to download</a>'
        st.markdown(linko_final, unsafe_allow_html=True)

    else:
        # Display the original markdown file content if df is None
        overview = read_markdown_file("pages/library_overview.md")
        st.markdown(overview, unsafe_allow_html=True)


with tab3:
    st.markdown("#### Moderator's Guide")
    st.markdown("ASK's mission is to provide USCG Auxiliary members efficient, accuracete and easy access to the authoritative source of knowledge on any topic in the Auxiliary.")
    st.markdown('If you would like to help ASK acheive this mission, **please reach out!**')
                
    st.markdown('''Presently, ASK works by analyzing documents that are the most current official policy that exists at a national level. 
             If you see a document missing from the libary or should be removed, please let us know.''')  
    
    st.markdown('''If you find an error or ommision in a response, please let me know. Be sure to include the exact question asked
             and a reference to the applicable policy (doc and page).''')  
                
    st.markdown('Send an email to uscgaux.drew@wks.us.''')

with tab4:
    roadmap = read_markdown_file("pages/roadmap.md")
    st.markdown(roadmap, unsafe_allow_html=True)
    
with tab5:
    st.markdown("#### Feedback")
    st.markdown("ASK's mission is to provide USCG Auxiliary members efficient, accuracete and easy access to the authoritative source of knowledge on any topic in the Auxiliary.")
    st.markdown('If you would like to help ASK acheive this mission, **please reach out!**')
                
    st.markdown('''Presently, ASK works by analyzing documents that are the most current official policy that exists at a national level. 
             If you see a document missing from the libary or should be removed, please let us know.''')  
    
    st.markdown('''If you find an error or ommision in a response, please let me know. Be sure to include the exact question asked
             and a reference to the applicable policy (doc and page).''')  
                
    st.markdown('Send an email to uscgaux.drew@wks.us.''')
