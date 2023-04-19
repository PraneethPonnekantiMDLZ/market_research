import streamlit as st
import PyPDF2
import re
import requests
from io import BytesIO

# Title of the Streamlit app
st.title("Annual Report Parser")

def process_pdf_file(pdf_file):
    """
    Process the PDF file and return the pages and highlighted occurrences of keywords.
    """
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.getNumPages()
    pages = []
    for i in range(num_pages):
        page = pdf_reader.getPage(i)
        text = page.extractText()
        pages.append(text)

    # Highlight the occurrences of the keywords
    keywords = st.text_input("Enter keywords (separated by commas)")
    highlights = {}
    if keywords:
        keywords_list = keywords.split(",")
        for keyword in keywords_list:
            occurrences = []
            for i, page in enumerate(pages):
                # Find all paragraphs that contain the keyword
                paragraphs = re.findall(r'(?:[^\n][\n]?){1,}(?:\b%s\b)(?:[^\n][\n]?){1,}' % keyword.strip(), page, flags=re.IGNORECASE)
                if paragraphs:
                    for paragraph in paragraphs:
                        # Highlight the keyword in the paragraph
                        highlighted_paragraph = paragraph.replace(keyword.strip(), f"<mark>{keyword.strip()}</mark>")
                        occurrences.append((i+1, highlighted_paragraph))
            if occurrences:
                highlights[keyword.strip()] = occurrences

    return pages, highlights


# Radio button to choose between uploading a file or entering a URL
option = st.radio("Choose an option", ("Upload a file", "Enter a URL"))

if option == "Upload a file":
    # File uploader to upload the annual report file
    uploaded_file = st.file_uploader("Choose an annual report file", type=["pdf"])
    if uploaded_file:
        # Display the file details
        st.write("File details:")
        st.write(uploaded_file.name)
        st.write(uploaded_file.size)

        # Process the annual report file
        pages, highlights = process_pdf_file(uploaded_file)

        # Display the highlighted occurrences of keywords
        for keyword, occurrences in highlights.items():
            st.write(f"Occurrences of '{keyword}' in the annual report:")
            for occurrence in occurrences:
                st.write(f"Page {occurrence[0]}")
                st.write(occurrence[1], unsafe_allow_html=True)

        # Paginate the annual report
        page_num = st.slider("Page", min_value=1, max_value=len(pages))
        st.write(pages[page_num-1])
else:
    # Text input to enter the URL of the PDF file
    pdf_url = st.text_input("Enter the URL of the PDF file")

    # Download the PDF file from the URL
    if pdf_url:
        response = requests.get(pdf_url)
        pdf_data = response.content
        pdf_file = BytesIO(pdf_data)

        # Process the annual report file
        pages, highlights = process_pdf_file(pdf_file)
 
         # Display the highlighted occurrences of keywords
        for keyword, occurrences in highlights.items():
            st.write(f"Occurrences of '{keyword}' in the annual report:")
            for occurrence in occurrences:
                st.write(f"Page {occurrence[0]}")
                st.write(occurrence[1], unsafe_allow_html=True)

        # Paginate the annual report
        page_num = st.slider("Page", min_value=1, max_value=len(pages))
        st.write(pages[page_num-1])
        
 
if __name__ == '__main__':
    main()
                
