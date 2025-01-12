import streamlit as st
import pdfplumber
import openai
import pandas as pd
from io import StringIO
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    #api_key = st.secrets["OPENAI_API_KEY"],
    api_key = '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',
)

# Define the function to get a response from OpenAI
def get_gpt_response(text):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that counts how many containers of Gewerbeabfall(Gewerbeabfall entleeren), Küchenabfälle(Kunststoffbehälter), Papierabfälle, and Restmüll have been disposed of. Check the menge of each entry as some have multiple in each entry."
            },
            {
                "role": "user",
                "content": f"""
                Given the following invoice text, calculate the number of containers for each type of waste mentioned:
                Gewerbeabfall
                Küchenabfälle

                Text:
                {text}

                Output the results in the following format:
                Anzahl Behälter
                Gewerbeabfall    [Total count]
                Küchenabfälle    [Total count]

                Additionally caculate the total cost of each type of waste and the volume of the containers.
                """
            }
        ],
        model="gpt-4-turbo",
    )
    # Access the content from the nested structure
    gpt_response = response.choices[0].message.content
    return gpt_response

# Define the main function for your Streamlit app
def main():
    # Set the page configuration
    st.set_page_config(
        layout="wide", 
        page_title="Wigo Ersparungen Rechner", 
        page_icon="♻️"
    )

    # Title of the app
    st.markdown("<h1 style='text-align: center; color: black;'>Wigo Ersparungen Rechner</h1>", unsafe_allow_html=True)

    # PDF uploader
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

    # Set up OpenAI API key
    openai.api_key = st.secrets["OPENAI_API_KEY"]  

    # Process PDF and interact with OpenAI
    if pdf_file is not None:
        with pdfplumber.open(pdf_file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
        
            if text:
                st.write("Processing your data with OpenAI...")
                gpt_response = get_gpt_response(text)
                
                st.write("Here is the result from the OpenAI model:")
                st.text_area("OpenAI Response", gpt_response, height=300)
                
                # Optionally, parse the GPT response into a DataFrame and display it
                try:
                    # Example: Assuming the response is a table in CSV format
                    df = pd.read_csv(StringIO(gpt_response), sep="|", engine="python")
                    st.write("Extracted Data:")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Failed to parse the response into a DataFrame: {e}")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
