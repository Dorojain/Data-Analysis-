# clean_paytm_reviews_1_2_3.py

import pandas as pd
import re
from datetime import datetime
from langdetect import detect, DetectorFactory

# To ensure consistent results from langdetect
DetectorFactory.seed = 0

# ---------------------------
# Step 1: Load existing CSV
# ---------------------------
csv_file = 'paytm_reviews_1_2_3.csv'  # your existing 1,2,3-star reviews CSV
df = pd.read_csv(csv_file)

print("\n📊 Initial data preview:\n")
print(df.head(10))
print(f"Total reviews loaded: {len(df)}")

# ---------------------------
# Step 2: Clean reviews
# ---------------------------

def is_meaningful(text):
    """
    Check if a review is meaningful:
    - Not empty
    - More than 1 word
    - Not just emojis or special characters
    """
    text = str(text).strip()
    if len(text.split()) <= 1:
        return False
    if re.fullmatch(r'[^\w\s]+', text):
        return False
    return True

# Apply cleaning
df['meaningful'] = df['content'].apply(is_meaningful)
df_clean = df[df['meaningful']].copy()
print(f"\n💡 Total meaningful reviews after cleaning: {len(df_clean)}")

# ---------------------------
# Step 3: Filter English reviews
# ---------------------------
def is_english(text):
    try:
        return detect(str(text)) == 'en'
    except:
        return False

df_clean['is_english'] = df_clean['content'].apply(is_english)
df_clean = df_clean[df_clean['is_english']]
print(f"💬 Total English reviews after filtering: {len(df_clean)}")

# ---------------------------
# Step 4: Optional date filtering
# ---------------------------
# Uncomment and edit the range if needed
# start_date = datetime(2025, 7, 1)
# end_date = datetime(2025, 9, 30)
# df_clean['at'] = pd.to_datetime(df_clean['at'])
# df_clean = df_clean[(df_clean['at'] >= start_date) & (df_clean['at'] <= end_date)]
# print(f"Total reviews after date filter: {len(df_clean)}")

# ---------------------------
# Step 5: Save cleaned CSV
# ---------------------------
cleaned_csv_file = 'paytm_reviews_1_2_3_clean_en.csv'
df_clean.to_csv(cleaned_csv_file, index=False)
print(f"💾 Saved cleaned English reviews to '{cleaned_csv_file}'")

# ---------------------------
# Step 6: Optional summary by rating
# ---------------------------
rating_counts = df_clean['score'].value_counts().sort_index()
print("\n⭐ Review counts by rating (1, 2, 3 stars):")
for rating, count in rating_counts.items():
    print(f"{rating}-star: {count}")
