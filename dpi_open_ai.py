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
# Custom CSS styles for Streamlit app
CUSTOM_CSS = """
<style>
/* Adjust the width of the main content area */
.reportview-container .main .block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Add padding to table cells */
table th, table td {
    padding: 0.5rem;
}

/* Add a border to table cells */
table th, table td {
    border: 1px solid #ddd;
}

/* Add some spacing between table cells */
table th, table td {
    margin: 0.1rem;
}

/* Center align the table */
table {
    margin-left: auto;
    margin-right: auto;
}

/* Add some padding to the input fields */
input[type="text"], input[type="password"], textarea, input[type="date"] {
    padding: 0.5rem;
}

/* Remove outline from input fields on focus */
input[type="text"]:focus, input[type="password"]:focus, textarea:focus, input[type="date"]:focus {
    outline: none;
}

/* Add some margin to the form inputs */
.form-input {
    margin-bottom: 1rem;
}

/* Add some margin to the submit button */
.form-submit-button {
    margin-top: 1rem;
}

</style>
"""


# Streamlit app
def main():
    
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.title("DPI using OpenAI") # Update with an appropriate title

    # Input for OpenAI API key
    api_key = st.text_input("OpenAI API Key:", type="password")

    # Input for statement
    statement = st.text_area("Statement:", value="")

    # Input for company name
    company_name = st.text_input("Company Name:", value="")

    # Input for business dimension
    business_dimension = st.text_input("Business Dimension:", value="")

    # Input for start date and end date for search results filtering
    start_date = st.date_input("Start Date:", value=(datetime.now() - timedelta(days=365)))
    end_date = st.date_input("End Date:", value=datetime.now())

    # Generate offerings and keywords
    offerings, keywords = generate_offerings_and_keywords(api_key, statement, company_name, business_dimension)

    # Generate Google search URL with date range filter
    google_search_url = generate_google_search_url(statement, company_name, business_dimension, start_date, end_date)

    # Display the generated data in a DataFrame
    data = {"Statement": [statement], "Company Name": [company_name], "Business Dimension": [business_dimension], "Offerings": [offerings], "Keywords": [keywords], "Google Search URL (Date Range)": [google_search_url]}
    df = pd.DataFrame(data)
    st.table(df)

if __name__ == "__main__":
    main()
