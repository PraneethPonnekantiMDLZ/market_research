import requests
import streamlit as st
import datetime
import urllib.parse

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
    brands = st.text_area("Enter Brand Names (comma separated)")
    brands = [brand.strip() for brand in brands.split(',') if brand.strip()]

    # Get current year
    current_year = datetime.datetime.now().year

    # Get current date
    current_date = datetime.datetime.now().date()

    # Calculate past year
    past_year = current_year - 1

    # Perform Google search
    if st.button("Search"):
        urls = []
        for brand in brands:
            # Construct search query with time frame
            search_query = f'{search_term} {" ".join(keywords)} after:{past_year}-01-01 before:{current_date}'
            if company_name:
                search_query = f'intext:"{company_name}" ' + search_query
            if website_name:
                search_query += f" site:{website_name}"
            search_query = search_query.replace(" ", "%20")
            if brand:
                search_query = f"{search_query} {brand}"
            url = f"https://www.google.com/search?q={search_query}"
            urls.append(url)

        # Display URLs in table
        st.subheader("Generated Google Search URLs for Brands:")
        table_data = []
        for i, url in enumerate(urls):
            brand_name = brands[i] if i < len(brands) else ""
            table_data.append((brand_name, url))
        st.table(table_data)

if __name__ == '__main__':
    main()
