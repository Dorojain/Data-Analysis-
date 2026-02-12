# Step 0: Import libraries
from google_play_scraper import reviews, Sort
import pandas as pd

# Step 1: Setup
app_id = 'net.one97.paytm'
batch_count = 500        # Number of reviews per fetch
max_reviews = 10000      # Total number of reviews to fetch (safeguard)
all_reviews = []
token = None
total_fetched = 0

print("🚀 Starting to fetch Paytm reviews...")

# Step 2: Fetch reviews in batches
while total_fetched < max_reviews:
    result, token = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,   # Fetch newest reviews first
        count=batch_count,
        continuation_token=token
    )

    if not result:
        break

    total_fetched += len(result)
    print(f"📦 Fetched {len(result)} reviews, total collected: {total_fetched}")

    # Append to list
    all_reviews.extend(result)

    # Stop if no more reviews
    if token is None:
        break

# Step 3: Convert to DataFrame
df = pd.DataFrame(all_reviews)
df = df[['userName', 'score', 'content', 'at']]
df['at'] = pd.to_datetime(df['at'])

# Step 4: Count reviews by rating
rating_counts = df['score'].value_counts().sort_index()
print("\n⭐ Review counts by rating:")
for rating in range(1, 6):
    count = rating_counts.get(rating, 0)
    print(f"{rating}-star: {count}")

# Step 5: Optionally filter 2- and 3-star reviews
df_2_3 = df[df['score'].isin([2, 3])]
print(f"\n✅ Total 2- and 3-star reviews: {len(df_2_3)}")
print(df_2_3.head(10))

# Step 6: Save to CSV
df.to_csv('paytm_all_reviews.csv', index=False)
df_2_3.to_csv('paytm_reviews_2_3.csv', index=False)
print("\n💾 Saved all reviews to 'paytm_all_reviews.csv'")
print("💾 Saved filtered 2- and 3-star reviews to 'paytm_reviews_2_3.csv'")

# Step 1: Filter reviews with ratings 1, 2, or 3
filtered_reviews = df[df['score'].isin([1, 2, 3])]

# Step 2: Print a sample of the filtered reviews
print("\n📊 Sample of 1-, 2-, 3-star reviews:\n")
print(filtered_reviews.head(10))

# Step 3: Show total count by rating
rating_counts = filtered_reviews['score'].value_counts().sort_index()
print("\n⭐ Review counts (1, 2, 3 stars):")
for rating, count in rating_counts.items():
    print(f"{rating}-star: {count}")

# Step 4: Save filtered reviews to CSV
filtered_reviews.to_csv('paytm_reviews_1_2_3.csv', index=False)
print("\n💾 Saved filtered 1-, 2-, 3-star reviews to 'paytm_reviews_1_2_3.csv'")

import pandas as pd
from datetime import datetime

# Step 1: Load the already fetched 1-, 2-, 3-star reviews
df = pd.read_csv('paytm_reviews_1_2_3.csv')

# Step 2: Convert 'at' column to datetime
df['at'] = pd.to_datetime(df['at'])

# Step 3: Define your date range
start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 9, 30)

# Step 4: Filter by date
df_filtered = df[(df['at'] >= start_date) & (df['at'] <= end_date)]

# Step 5: Check results
print(df_filtered.head(10))
print(f"✅ Total reviews in this period: {len(df_filtered)}")

# Step 6: Save to CSV
df_filtered.to_csv('paytm_reviews_1_2_3_JulSep2025.csv', index=False)
print("💾 Saved filtered reviews to 'paytm_reviews_1_2_3_JulSep2025.csv'")

