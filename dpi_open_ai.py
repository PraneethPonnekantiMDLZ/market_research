import streamlit as st
import openai
import pandas as pd
from datetime import datetime, timedelta

# Set up OpenAI API credentials
openai.api_key = "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"  # Replace with your actual OpenAI API key

# Phases of the consumer journey
phases = [
    "Initial Consideration",
    "Active Evaluation",
    "Moment of Purchase",
    "Post-Purchase",
    # Add more phases as needed
]

# Function to generate offerings and associated keywords using OpenAI API
def generate_offerings_and_keywords(phase, company_name):
    # TODO: Replace with your own logic to generate offerings and keywords using OpenAI API
    offerings = openai.Completion.create(
        prompt=f"Generate offerings for {phase} phase of consumer journey for {company_name}",
        engine="text-davinci-002",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    keywords = openai.Completion.create(
        prompt=f"Generate keywords for {phase} phase of consumer journey for {company_name}",
        engine="text-davinci-002",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return offerings.choices[0].text.strip(), keywords.choices[0].text.strip()

# Function to generate Google search URL with date range filter
def generate_google_search_url(phase, company_name, start_date, end_date):
    # TODO: Replace with your own logic to generate Google search URL with appropriate date range filter
    url = f"https://www.google.com/search?q={company_name} {phase} phase of consumer journey&date={start_date}:{end_date}"
    return url

# Streamlit app
def main():
    st.title("Consumer Journey and Offerings")

    # Input for phase of consumer journey
    phase = st.selectbox("Phase of Consumer Journey:", phases)

    # Input for company name
    company_name = st.text_input("Company Name:", value="", key="company_name_input")

    # Input for start date and end date for search results filtering
    start_date = st.date_input("Start Date:", value=(datetime.now() - timedelta(days=365)), key="start_date_input")
    end_date = st.date_input("End Date:", value=datetime.now(), key="end_date_input")

    # Generate offerings and keywords
    offerings, keywords = generate_offerings_and_keywords(phase, company_name)

    # Generate Google search URL with date range filter
    google_search_url = generate_google_search_url(phase, company_name, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    # Display the generated data in a DataFrame
    data = {"Phase of Consumer Journey": [phase], f"{company_name} Offerings": [offerings], "Keywords": [keywords], "Google Search URL (Past Year)": [google_search_url]}
    df = pd.DataFrame(data)
    st.table(df)

if __name__ == "__main__":
    main()
