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

def generate_keywords(statement, company_name, business_dimension, start_date, end_date):
    # TODO: Replace with your own logic to generate keywords using OpenAI API
    keywords = openai.Completion.create(
        prompt=f"Generate keywords for {business_dimension} {statement} for {company_name}",
        engine="text-davinci-002",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    keywords_list = keywords.choices[0].text.strip().split(",") # Convert string of keywords to a list
    return keywords_list

# Function to generate Google search URL with date range filter
def generate_google_search_url(statement, company_name, business_dimension, start_date, end_date, keywords):
    # Format the company name with double quotes
    company_name = f'"{company_name}"'
    # Get current year
    current_year = datetime.now().year

    # Get current date
    current_date = datetime.now().date()

    # Calculate past year
    past_year = current_year - 1
    
    # Convert keywords from string to list
    keywords_list = keywords.split(",")
    
    # Generate the Google search URL
    url = f'https://www.google.com/search?q={company_name} {business_dimension} {" ".join(keywords_list)} after:{past_year}-01-01 before:{current_date}'
    return url

def main():
    #st.title("DPI using OpenAI") # Update with an appropriate title
    
    st.set_page_config(page_title="DPI using OpenAI", page_icon=":rocket:", layout="wide") # Update with appropriate title and icon
    
    # Create collapsible input bar
     with st.sidebar.beta_expander("DPI Inputs", expanded=True):
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
        
        # Input for custom keywords
        custom_keywords = st.text_input("Custom Keywords (comma-separated):", value="")
        
        # Input for start date
        start_date = st.date_input("Start Date:", value=(datetime.now() - timedelta(days=365)).date())

        # Input for end date
        end_date = st.date_input("End Date:", value=datetime.now().date())
        
        # Button to generate output
        generate_button = st.button("Generate Output")
           
    # Output section with full screen width
    st.markdown('<div class="collapsible-content"></div>', unsafe_allow_html=True)
    st.write("Output:")
    st.markdown('<div style="overflow-x:auto; margin-top: 20px;">', unsafe_allow_html=True)
    
    # Display generated keywords separately
    if generate_button:
        if statement and company_name and business_dimension and start_date and end_date:
                offerings, keywords = generate_offerings_and_keywords(api_key, statement, company_name, business_dimension)
                st.markdown(f"**Generated Offerings:**\n{offerings}")
                st.markdown(f"**Generated Keywords:**\n{keywords}")
                st.markdown('<br>', unsafe_allow_html=True)
            
                if custom_keywords:
                    custom_keywords_list = [keyword.strip() for keyword in custom_keywords.split(",")]
                    st.markdown(f"**Custom Keywords:**\n{', '.join(custom_keywords_list)}")
                    st.markdown('<br>', unsafe_allow_html=True)
    
    # Display Google search URL with date range filter for generated keywords
    if generate_button : 
        if statement and company_name and business_dimension and start_date and end_date:
            generated_kw = generate_keywords(statement, company_name, business_dimension, start_date, end_date)
            google_search_url_generated = generate_google_search_url(statement, company_name, business_dimension, start_date, end_date, generated_kw)
            st.markdown(f"**Google Search URL with Date Range Filter (Generated Keywords):**\n{google_search_url_generated}")
            st.markdown('<br>', unsafe_allow_html=True)
            
            if custom_keywords:
                custom_keywords_list = [keyword.strip() for keyword in custom_keywords.split(",")]
                google_search_url_custom = generate_google_search_url(statement, company_name, business_dimension, start_date, end_date, custom_keywords_list)
                st.markdown(f"**Google Search URL with Date Range Filter (Custom Keywords):**\n{google_search_url_custom}")
                st.markdown('<br>', unsafe_allow_html=True)
    
    # Display table with search results for generated keywords
    if generate_button : 
           if statement and company_name and business_dimension and start_date and end_date:
                df = generate_search_results(statement, company_name, business_dimension, start_date, end_date)
                st.write(df)
    
    st.markdown('</div>', unsafe_allow_html=True)




if __name__ == "__main__":
    main()

