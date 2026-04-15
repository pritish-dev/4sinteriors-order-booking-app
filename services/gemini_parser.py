import google.generativeai as genai
import pandas as pd
import json
import time
import os
from utils.config import get_secret

# ✅ Setup API key properly
api_key = get_secret("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing")

# Force fallback support
os.environ["GOOGLE_API_KEY"] = api_key

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_price_with_gemini(pdf_bytes):
    prompt = """
    Extract all LN CODE and MRP from this furniture price list PDF.

    Return ONLY JSON format:
    [
      {"LN_CODE": "ABC123", "MRP": 45000}
    ]
    """

    for attempt in range(3):
        try:
            response = model.generate_content(
                [
                    prompt,
                    {"mime_type": "application/pdf", "data": pdf_bytes.read()}
                ]
            )

            data = json.loads(response.text)
            return pd.DataFrame(data)

        except Exception as e:
            if "429" in str(e):
                wait_time = 15 * (attempt + 1)
                print(f"Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    return pd.DataFrame(columns=["LN_CODE", "MRP"])