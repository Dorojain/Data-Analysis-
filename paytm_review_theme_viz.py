# paytm_review_theme_viz.py

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# -------------------------------
# Step 1: Load the cleaned CSV
# -------------------------------
df = pd.read_csv("paytm_reviews_1_2_3_clean_en.csv")

print("📊 Initial data preview:\n")
print(df.head(10))
print(f"\nTotal reviews loaded: {len(df)}")

# -------------------------------
# Step 2: Generate Word Cloud
# -------------------------------
all_text = " ".join(df['content'].astype(str))

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    max_words=100
).generate(all_text)

# Show word cloud in a separate window
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Frequent Words in 1-,2-,3-Star Reviews", fontsize=16)
plt.show()

# Save word cloud as PNG
wordcloud.to_file("paytm_wordcloud.png")
print("💾 Word cloud saved as 'paytm_wordcloud.png'")

# -------------------------------
# Step 3: Thematic Analysis with TF-IDF + KMeans
# -------------------------------
tfidf = TfidfVectorizer(max_features=500, stop_words='english')
X = tfidf.fit_transform(df['content'].astype(str))

# Elbow method to find optimal k
inertia_list = []
k_values = range(2, 10)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    inertia_list.append(kmeans.inertia_)

# Show elbow plot in a separate window
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia_list, marker='o')
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method to Find Optimal k")
plt.grid(True)
plt.show()

# Save elbow plot as PNG
plt.savefig("paytm_elbow_plot.png")
print("💾 Elbow plot saved as 'paytm_elbow_plot.png'")

# -------------------------------
# Step 4: Apply KMeans for thematic clustering (example with k=4)
# -------------------------------
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=0)
df['cluster'] = kmeans.fit_predict(X)

# Print top words per cluster
terms = tfidf.get_feature_names_out()
for i in range(optimal_k):
    cluster_terms = [terms[ind] for ind in kmeans.cluster_centers_.argsort()[i, -10:]]
    print(f"\nCluster {i+1} top terms: {cluster_terms}")

# Save clustered data
df.to_csv("paytm_reviews_clustered.csv", index=False)
print("💾 Clustered reviews saved to 'paytm_reviews_clustered.csv'")
