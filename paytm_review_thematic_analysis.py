# Filename: paytm_review_thematic_analysis.py
# Purpose: Perform TF-IDF-based thematic clustering on *all* Paytm reviews

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load cleaned reviews (all ratings)
df = pd.read_csv("paytm_reviews_all_clean_en.csv")

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X = tfidf.fit_transform(df['cleaned_review'])

# Use optimal K (e.g., 4 or 5 — you can tune this again)
k = 5
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Top words per cluster
terms = tfidf.get_feature_names_out()
for i in range(k):
    cluster_terms = [terms[ind] for ind in kmeans.cluster_centers_[i].argsort()[-10:]]
    print(f"Cluster {i+1} top words:", cluster_terms)

# Save clustered data
df.to_csv("paytm_reviews_all_clustered.csv", index=False)
print("💾 Clustered reviews saved to 'paytm_reviews_all_clustered.csv'")

# Optional: visualize cluster word clouds
for i in range(k):
    cluster_text = " ".join(df[df['cluster'] == i]['cleaned_review'])
    wc = WordCloud(width=800, height=400, background_color='white').generate(cluster_text)
    plt.figure()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Cluster {i+1} WordCloud")
    plt.show()
