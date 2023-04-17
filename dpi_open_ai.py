import streamlit as st
import openai
import pandas as pd
from datetime import datetime, timedelta

# Function to generate offerings and associated keywords using OpenAI API
def generate_offerings_and_keywords(api_key, statement, company_name, business_dimension):
    # Set up OpenAI API credentials
    openai.api_key = api_key
    
    # TODO: Replace with your own logic to generate offerings and keywords using OpenAI API
    offerings = openai.Completion.create(
        prompt=f"Generate offerings for {business_dimension} {statement} for {company_name}",
        engine="text-davinci-002",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    keywords = openai.Completion.create(
        prompt=f"Generate keywords for {business_dimension} {statement} for {company_name}",
        engine="text-davinci-002",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return offerings.choices[0].text.strip(), keywords.choices[0].text.strip()

# Function to generate Google search URL with date range filter
def generate_google_search_url(statement, company_name, business_dimension, start_date, end_date):
    # Format the company name with double quotes
    company_name = f'"{company_name}"'
    
    # Format the dates with after: and before: parameters
    dates = f'after:{start_date.strftime("%Y-%m-%d")}%20before:{end_date.strftime("%Y-%m-%d")}'
    
    # Generate the Google search URL
    url = f"https://www.google.com/search?q={business_dimension} {company_name} {statement}&{dates}"
    return url

# Streamlit app
def main():
    
    #st.title("DPI using OpenAI") # Update with an appropriate title
    st.set_page_config(page_title="DPI using OpenAI", page_icon=":rocket:", layout="wide") # Update with appropriate title and icon
    
        # Create collapsible input bar
    with st.beta_expander("Input", expanded=True):
        # Input for OpenAI API key
        api_key = st.text_input("OpenAI API Key:", type="password")
        
        # Input for company name
        company_name = st.text_input("Company Name:", value="")

        # Input for business dimension
        business_dimension = st.selectbox("Business Dimension:", options=["Commercial Optimization",
                                            "Consumer Experience",
                                            "Consumer Insight",
                                            "Customer Experience",
                                            "Digital Back Office",
                                            "Digital Commerce",
                                            "Digital Marketing",
                                            "Innovation & Smart R&D",
                                            "Smart Supply Chain & Manufacturing",
                                            "Workforce of the future"]
                                         )
        
        # Input for statement
        statement = st.text_area("Statement:", value="")
        
        # Set start date to Jan 1, 2022
        start_date = datetime.date(2022, 1, 1)

        # Set end date to today's date
        end_date = datetime.date.today()
        
        # Button to generate output
        generate_button = st.button("Generate Output")
           
        
    # Output section with full screen width
    st.markdown('<div class="collapsible-content"></div>', unsafe_allow_html=True)
    st.write("Output:")
    st.markdown('<div style="overflow-x:auto; margin-top: 20px;">', unsafe_allow_html=True)
    # Display Google search URL with date range filter
    if generate_button : 
        if statement and company_name and business_dimension and start_date and end_date:
            google_search_url = generate_google_search_url(statement, company_name, business_dimension, start_date, end_date)
            st.markdown(f"**Google Search URL with Date Range Filter:**\n{google_search_url}")
            st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
