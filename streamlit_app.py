# import streamlit as st
# import random

# st.title("Career Planning 👩‍💻")

# early_pay = st.text_input("Enter your early career pay ($):")
# mid_career = st.text_input("Enter your mid-career pay ($):")

# if st.button("Check Fulfillment"):
#     fulfillment_rate = round(random.random(), 2)
#     st.metric(label="Fulfillment Rate", value=f"{fulfillment_rate*100:.0f}%")

#     if fulfillment_rate <= 0.5:
#         st.warning("😕 Looks like you are not very satisfied with your job.")
#     else:
#         st.success("😄 You are really enjoying it!")
import os
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
import random
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Career Fulfillment Clustering", layout="wide")

st.title("👩‍💻 Career Planning: U.S Post College Salaries According to Major and Degree")
st.header("Information about the project:")
st.write("This is the final project for course I310D: Intro to Human-Centered Data Science" +
         "It is produced by Team Data Devils, formerly known as Team MANS.")
st.write("Simply type in your actual or projected early career pay, and actual or projected career pay" +
         "You would be able to find out whether or not you are satisfied with your career choice!")

# Upload or Load data
@st.cache_data
def load_data():
    df = pd.read_csv("final-post-college-salaries.csv")
    df.drop(columns=["Degree Type"], axis=1, inplace=True)
    return df

df = load_data()

# Dictionary and cleaning functions
dic = {
    'Engineering': ["engineering"],
    'Computer': ['computer', 'informatics', 'software', 'information','data'],
    'Design': ['design', 'architecture', 'urban'],
    'Business': ['business', 'finance', 'accounting', 'management', 'marketing', 'economics', 'commerce'],
    'Math': ['math', 'statistics', 'actuarial'],
    'Physical Science': ['physics', 'chemistry', 'astronomy', 'geology', 'geophysics', 'material'],
    'Life Science': ['biology', 'biochemistry', 'neuroscience', 'microbiology', 'botany', 'zoology'],
    'Environment': ['environment', 'environmental', 'ecology', 'climate', 'sustainability'],
    'Health': ['nursing', 'health', 'medicine', 'pharmacy', 'medical', 'dental', 'veterinary', 'clinical', 'therapy', 'public health'],
    'Social Science': ['sociology', 'psychology', 'political', 'international', 'criminology', 'anthropology'],
    'Communication': ['communication', 'journalism', 'media', 'broadcasting', 'public relations'],
    'Arts': ['art', 'music', 'film', 'dance', 'theater', 'performing'],
    'Humanities': ['history', 'philosophy', 'literature', 'language', 'linguistics', 'classics', 'religion', 'ethics', 'cultural'],
    'Education': ['education', 'teaching', 'pedagogy', 'curriculum'],
    'Law': ['law', 'legal', 'criminology'],
    'General Science': ['general science', 'science'],
    'Service': ['hospitality', 'tourism', 'recreation', 'culinary', 'personal services'],
}


def to_int(value):
    value = value.replace("$", "").replace(",", "").replace("%", "")
    return int(value)

def assign_college(name):
    for key, list_key_words in dic.items():
        for key_word in list_key_words:
            if key_word.lower() in name.lower():
                return key
    return "Other"

def convert_percentage(value):
    return int(value) / 100

# Clean the dataframe
df["College"] = df["Major"].apply(assign_college)
df["Early Career Pay"] = df["Early Career Pay"].apply(to_int)
df["Mid-Career Pay"] = df["Mid-Career Pay"].apply(to_int)
df = df.drop(df[df["% High Meaning"] == "-"].index)
df["% High Meaning"] = df["% High Meaning"].apply(to_int).apply(convert_percentage)

# --- User Input ---
st.header("💬 Enter Your Own Career Data:")

early_pay = st.number_input("Enter your Early Career Pay ($)", min_value=0)
mid_career = st.number_input("Enter your Mid Career Pay ($)", min_value=0)
fulfillment_rate = st.slider("Rate your job fulfillment (0-100%)", 0, 100, 50) / 100

# --- Clustering ---
X = df[["Early Career Pay", "Mid-Career Pay", "% High Meaning"]].to_numpy()

kmeans_model = KMeans(n_clusters=4, random_state=0, n_init=1)
kmeans_model.fit(X)
labels = kmeans_model.labels_
center = kmeans_model.cluster_centers_

# --- 3D Plot ---
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

cluster_0 = (labels==0)
cluster_1 = (labels==1)
cluster_2 = (labels==2)
cluster_3 = (labels==3)

ax.scatter(X[cluster_0, 0], X[cluster_0, 1], X[cluster_0, 2], c='blue', label='Cluster 1', s=40)
ax.scatter(X[cluster_1, 0], X[cluster_1, 1], X[cluster_1, 2], c='orange', label='Cluster 2', s=40)
ax.scatter(X[cluster_2, 0], X[cluster_2, 1], X[cluster_2, 2], c='pink', label='Cluster 3', s=40)
ax.scatter(X[cluster_3, 0], X[cluster_3, 1], X[cluster_3, 2], c='green', label='Cluster 4', s=40)

# User input point
ax.scatter(int(early_pay), int(mid_career), float(fulfillment_rate), c='black', s=200, marker='D', label='Your Input')

ax.set_xlabel("Early Career Pay")
ax.set_ylabel("Mid Career Pay")
ax.set_zlabel("% High Meaning")
ax.set_title("3D Clustering of Careers")
ax.legend()

st.pyplot(fig)

# --- 2D Plot Pay Growth ---
df["Pay Growth"] = df["Mid-Career Pay"] - df["Early Career Pay"]
A = df[["Pay Growth", "% High Meaning"]].to_numpy()

kmeans2 = KMeans(n_clusters=4, random_state=0)
clusters2 = kmeans2.fit_predict(A)
centers2 = kmeans2.cluster_centers_

fig2 = plt.figure(figsize=(10,10))
ax2 = fig2.add_subplot(111)

for cluster_id in np.unique(clusters2):
    idx = clusters2 == cluster_id
    ax2.scatter(A[idx, 0], A[idx, 1], s=40, label=f"Cluster {cluster_id+1}", alpha=0.6)

ax2.scatter(centers2[:,0], centers2[:,1], c='red', s=200, marker='X', label='Centroids')

user_pay_growth = int(mid_career) - int(early_pay)
ax2.scatter(user_pay_growth, fulfillment_rate, c='black', s=100, marker='D', label='Your Input')

ax2.set_xlabel("Pay Growth ($)")
ax2.set_ylabel("% High Meaning")
ax2.set_title("KMeans Clustering: Pay Growth vs Fulfillment")
ax2.legend()

st.pyplot(fig2)
