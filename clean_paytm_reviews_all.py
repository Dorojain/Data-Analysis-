# Filename: clean_paytm_reviews_all.py
# Purpose: Clean all Paytm reviews (1–5 stars)

import pandas as pd
import re
from langdetect import detect
from tqdm import tqdm

tqdm.pandas()

# Load raw dataset
df = pd.read_csv("paytm_all_reviews.csv")

# Define text cleaning function
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # remove links
    text = re.sub(r"[^a-zA-Z\s]", "", text)              # remove numbers/punctuation
    text = re.sub(r"\s+", " ", text).strip()             # normalize spaces
    return text

# Detect English reviews only
def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

df["content"] = df["content"].astype(str)
df["cleaned_review"] = df["content"].progress_apply(clean_text)
df["is_english"] = df["cleaned_review"].progress_apply(is_english)
df_clean = df[df["is_english"] == True].copy()

print(f"✅ Cleaned reviews retained: {len(df_clean)} / {len(df)}")

# Save cleaned dataset
df_clean.to_csv("paytm_reviews_all_clean_en.csv", index=False)
print("💾 Cleaned dataset saved as 'paytm_reviews_all_clean_en.csv'")
