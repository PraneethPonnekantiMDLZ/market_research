import requests
from bs4 import BeautifulSoup
import streamlit as st
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Function to check if keywords are found in content
def check_keywords_in_content(content, keywords):
    for keyword in keywords:
        if keyword.lower() in content.lower():
            return True
    return False

# Function to generate recommended keywords using ML
def generate_keywords(description, search_term, num_keywords):
    # Combine description and search term
    text = description + " " + search_term

    # Vectorize text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])

    # Perform K-means clustering to group words
    kmeans = KMeans(n_clusters=num_keywords)
    kmeans.fit(tfidf_matrix)
    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    # Get top keywords from centroids
    keywords = []
    for i in sorted_centroids[0]:
        keywords.append(vectorizer.get_feature_names()[i])

    return keywords

# Streamlit web app
def main():
    st.title("Market Research Web App")

    # Input parameters
    company_name = st.text_input("Enter Company Name")
    search_term = st.text_input("Enter Search Term")
    description = st.text_area("Enter Description")
    keywords_manual = st.text_area("Enter Additional Keywords (comma separated)")
    num_keywords = st.slider("Number of Recommended Keywords", 5, 20, 10)

    # Generate recommended keywords
    keywords_auto = generate_keywords(description, search_term, num_keywords)

    # Combine manual and auto-generated keywords
    keywords_manual = [kw.strip() for kw in keywords_manual.split(',') if kw.strip()]
    keywords = list(set(keywords_auto + keywords_manual))[:num_keywords]

    # Get current year
    current_year = datetime.datetime.now().year

    # Get current date
    current_date = datetime.datetime.now().date()

    # Perform Google search
    if st.button("Search"):
        # Construct search query with time frame
        search_query = f'intext:"{company_name}" {search_term} {" ".join(keywords)} site:google.com after:{current_year - 1}-01-01 before:{current_date}'
        search_query = search_query.replace(" ", "%20")
        st.write("Search Query: ", search_query)
        url = f"https://www.google.com/search?q={search_query}"
        st.write("URL: ", url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Capture relevant links
        links = []
        for result in soup.find_all("div", class_="r"):
            link = result.find("a")
            if link:
                href = link.get("href")
                st.write("href : ", href)
                if href.startswith("/url?q="):
                    page_url = href[7:]
                    page_response = requests.get(page_url)
                    page_soup = BeautifulSoup(page_response.text, "html.parser")
                    page_content = page_soup.prettify()
                    if check_keywords_in_content(page_content, keywords):
                        links.append(page_content)

        # Display captured content
        st.subheader("Captured Content:")
        for content in links:
            st.code(content, language='html')

if __name__ == '__main__':
    main
