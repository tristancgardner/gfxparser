
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import re
import base64
import htmlTest_3_NP as parser
# ... The process_html_full_integration function ...

def streamlit_app():
    st.title("HTML File Processor")
    uploaded_file = st.file_uploader("Upload an HTML file", type=["html"])

    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        
        # Process the HTML content
        df_master = parser.process_html_full_integration(file_content)
        
        # Check if df_master is not None before proceeding
        if df_master is not None:
            # Display the processed dataframe
            st.dataframe(df_master)
            
            # Provide a link to download the processed data as CSV
            csv = df_master.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="MasterGraphics_EXO_NP.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("An error occurred while processing the HTML file. Please ensure the file format is correct.")

if __name__ == "__main__":
    streamlit_app()
