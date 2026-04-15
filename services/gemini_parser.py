import google.generativeai as genai
import pandas as pd
import json
from utils.config import get_secret

genai.configure(api_key=get_secret("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_price_with_gemini(pdf_bytes):
    prompt = """
    Extract all LN CODE and MRP from this furniture price list PDF.

    Return ONLY JSON format:
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