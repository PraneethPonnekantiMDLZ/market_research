import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to check if keywords are found in content
def check_keywords_in_content(content, keywords):
    for keyword in keywords:
        if keyword.lower() in content.lower():
            return True
    return False

# Streamlit web app
def main():
    st.title("Market Research Web App")

    # Input parameters
    company_name = st.text_input("Enter Company Name")
    search_term = st.text_input("Enter Search Term")
    keywords = st.text_area("Enter Associated Keywords (comma separated)")
    timeframe = st.text_input("Enter Timeframe (e.g., 2022-2023)")

    # Convert keywords to list
    keywords = [kw.strip() for kw in keywords.split(',') if kw.strip()]

    # Perform Google search
    if st.button("Search"):
        search_query = f"intext:{company_name} {search_term} {' '.join(keywords)} {timeframe} site:google.com"
        search_query = search_query.replace(" ", "%20")
        st.write("Search Quer : ", search_query)
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
                if href.startswith("/url?q="):
                    page_url = href[7:]
                    page_response = requests.get(page_url)
                    page_soup = BeautifulSoup(page_response.text, "html.parser")
                    page_content = page_soup.get_text()
                    if check_keywords_in_content(page_content, keywords):
                        links.append(page_url)

        # Display captured links
        st.subheader("Captured Links:")
        for link in links:
            st.write(link)

if __name__ == '__main__':
    main()
