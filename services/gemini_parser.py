import google.generativeai as genai
import streamlit as st
import pandas as pd

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_price_with_gemini(pdf_bytes):
    prompt = """
    You are given a furniture price list PDF.

    Extract all rows with:
    - LN CODE
    - MRP

    Return ONLY JSON in this format:
    [
      {"LN_CODE": "ABC123", "MRP": 45000},
      ...
    ]
    """

    response = model.generate_content(
        [
            prompt,
            {"mime_type": "application/pdf", "data": pdf_bytes.read()}
        ]
    )

    text = response.text

    try:
        import json
        data = json.loads(text)
        return pd.DataFrame(data)
    except:
        return pd.DataFrame(columns=["LN_CODE", "MRP"])