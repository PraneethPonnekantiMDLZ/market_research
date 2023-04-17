import streamlit as st
import openai
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import spacy

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

# Function to visit a URL and extract relevant information based on keywords
def visit_url_and_extract_info(url, keywords):
    # Send a request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all the links from the search results
    search_results = soup.find_all('a')
    evidence = ''
    evidence_links = []
    
    # Loop through the search results and extract information based on keywords
    for link in search_results:
        link_text = link.get_text()
        link_url = link.get('href')
        
        # Extract relevant information based on keywords
        if any(keyword in link_text.lower() for keyword in keywords.lower().split(',')):
            evidence += f"{link_text}\n"
            evidence_links.append(link_url)
    
    return evidence, evidence_links

# Streamlit app
def main():
    st.title("DPI using OpenAI") # Update with an appropriate title

    # Load spaCy NER model
    nlp = spacy.load("en_core_web_sm")

    # Input for OpenAI API key
    api_key = st.text_input("OpenAI API Key:", type="password")

    # Input for statement
    statement = st.text_area("Statement:", value="")

    # Input for company name
    company_name = st.text_input("Company Name:", value="")

    # Input for business dimension
    business_dimension = st.text_input("Business Dimension:", value="")

    # Input for start date and end date for search results filtering
    start_date = st.date_input("Start Date:", value=(datetime.now() - timedelta(days=365)).date())
    end_date = st.date_input("End Date:", value=datetime.now().date())

    # Button to trigger the search and extraction process
    if st.button("Extract Evidence"):
        # Call the functions to generate offerings and keywords
        offerings, keywords = generate_offerings_and_keywords(api_key, statement, company_name, business_dimension)

        # Generate the Google search URL with date range filter
        url = generate_google_search_url(statement, company_name, business_dimension, start_date, end_date)

        # Visit the URL and extract relevant information based on keywords
        evidence, evidence_links = visit_url_and_extract_info(url, keywords)

        # Perform NER on extracted evidence
        evidence_ner = perform_ner(evidence, nlp)

        # Extract keywords from NER results
        extracted_keywords = extract_keywords_from_ner(evidence_ner)

        # Store the extracted evidence and evidence links in a dataframe
        df = pd.DataFrame({"evidence": [evidence], "evidence_links": [evidence_links],
                           "keywords": [extracted_keywords]})

        # Display the extracted evidence, evidence links, and keywords in Streamlit
        st.subheader("Extracted Evidence:")
        st.write(df)

def perform_ner(text, nlp):
    """Perform named entity recognition (NER) using spaCy"""
    doc = nlp(text)
    evidence_ner = []
    for ent in doc.ents:
        evidence_ner.append({"text": ent.text, "label": ent.label_})
    return evidence_ner

def extract_keywords_from_ner(ner_results):
    """Extract keywords from NER results"""
    keywords = []
    for result in ner_results:
        if result["label"] in ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART"]:
            keywords.append(result["text"])
    return keywords


