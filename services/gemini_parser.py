import google.generativeai as genai
import streamlit as st
import pandas as pd
import json

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_price_with_gemini(pdf_bytes):
    prompt = """
    Extract all LN CODE and MRP from this furniture price list PDF.

    Return ONLY valid JSON:
    [
      {"LN_CODE": "ABC123", "MRP": 45000}
    ]
    """

    response = model.generate_content(
        [
            prompt,
            {"mime_type": "application/pdf", "data": pdf_bytes.read()}
        ]
    )

    try:
        data = json.loads(response.text)
        return pd.DataFrame(data)
    except:
        return pd.DataFrame(columns=["LN_CODE", "MRP"])