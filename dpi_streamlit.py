import requests
from bs4 import BeautifulSoup
import streamlit as st
import datetime

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
    keywords = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    website_name = st.text_input("Search in a specific website Name (Optional)")
    
    # Get current year
    current_year = datetime.datetime.now().year

    # Get current date
    current_date = datetime.datetime.now().date()

    # Calculate past year
    past_year = current_year - 1

    # Perform Google search
    if st.button("Search"):
        # Construct search query with time frame
        search_query = f'intext:"{company_name}" {search_term} {" ".join(keywords)} after:{past_year}-01-01 before:{current_date}'
        if website_name:
            search_query += f" site:{website_name}"
        search_query = search_query.replace(" ", "%20")
        #st.write("Search Query: ", search_query)
        url = f"https://www.google.com/search?q={search_query}"
        #st.write("URL: ", url)
        st.markdown("### Generated Google Search URL:")
        with st.beta_container():
            st.markdown(f"[{url}]({url})")
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
    main()
