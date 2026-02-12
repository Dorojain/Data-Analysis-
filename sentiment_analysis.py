# Filename: sentiment_analysis.py
# Purpose: Perform overall sentiment analysis on Paytm reviews

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# 1️⃣ Load data
print("🔍 Loading cleaned Paytm reviews...")
df = pd.read_csv("paytm_reviews_1_2_3_clean_en.csv")

# 2️⃣ Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# 3️⃣ Define a function for sentiment classification
def get_sentiment(text):
    if not isinstance(text, str):
        return "Neutral"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.3:
        return "Positive"
    elif score <= -0.3:
        return "Negative"
    else:
        return "Neutral"

# 4️⃣ Apply sentiment analysis to all reviews
print("⚙️  Calculating sentiment scores...")
df["sentiment"] = df["content"].apply(get_sentiment)

# 5️⃣ Display counts for verification
sentiment_counts = df["sentiment"].value_counts()
print("\n📊 Sentiment distribution:")
print(sentiment_counts)

# 6️⃣ Define custom colors for each sentiment
color_map = {
    "Negative": "red",
    "Positive": "green",
    "Neutral": "grey"
}

# 7️⃣ Plot sentiment distribution
print("\n📈 Displaying sentiment graph...")
sentiment_counts.plot(
    kind="bar",
    color=[color_map.get(s, "grey") for s in sentiment_counts.index],
    figsize=(6, 4),
    edgecolor="black"
)

plt.title("Sentiment Distribution of Paytm Reviews", fontsize=14)
plt.xlabel("Sentiment", fontsize=12)
plt.ylabel("Number of Reviews", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 8️⃣ Save the result
df.to_csv("paytm_reviews_with_sentiment.csv", index=False)
print("\n💾 Sentiment analysis saved to 'paytm_reviews_with_sentiment.csv'")
