# --------------------------------------------------
# ✅ MOVIE RECOMMENDATION MODEL TRAINING SCRIPT
# --------------------------------------------------

import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# --------------------------------------------------
# ✅ STEP 1 — LOAD DATA
# --------------------------------------------------

df = pd.read_csv("dataset.csv")
print("✅ Dataset Loaded:", df.shape)


# --------------------------------------------------
# ✅ STEP 2 — CLEAN & CONVERT LIST COLUMNS
# --------------------------------------------------

def safe_convert(obj):
    if isinstance(obj, str):
        try:
            return ast.literal_eval(obj)
        except:
            return []
    return obj

df['genres'] = df['genres'].apply(safe_convert)
df['cast'] = df['cast'].apply(safe_convert)
df['crew'] = df['crew'].apply(safe_convert)


# --------------------------------------------------
# ✅ STEP 3 — EXTRACT USEFUL FEATURES
# --------------------------------------------------

# top 3 cast
df['cast'] = df['cast'].apply(lambda x: x[:3] if x else [])

# extract director from crew list
def get_director(crew_list):
    if not crew_list:
        return []
    return [person for person in crew_list if "director" in person.lower()][:1]

df['director'] = df['crew'].apply(get_director)


# --------------------------------------------------
# ✅ STEP 4 — CONVERT LISTS TO STRINGS
# --------------------------------------------------

df['genres'] = df['genres'].apply(lambda x: " ".join(x))
df['cast'] = df['cast'].apply(lambda x: " ".join(x))
df['director'] = df['director'].apply(lambda x: " ".join(x))
df['overview'] = df['overview'].fillna("")


# --------------------------------------------------
# ✅ STEP 5 — CREATE TAGS COLUMN
# --------------------------------------------------

df['tags'] = (
    df['overview'] + " " +
    df['genres'] + " " +
    df['cast'] + " " +
    df['director']
)

print("✅ Tags Column Created")
print(df[['title', 'tags']].head())


# --------------------------------------------------
# ✅ STEP 6 — TF-IDF VECTORIZATION
# --------------------------------------------------

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(df['tags']).toarray()

print("✅ Vectorization Complete:", vectors.shape)


# --------------------------------------------------
# ✅ STEP 7 — COSINE SIMILARITY MATRIX
# --------------------------------------------------

similarity = cosine_similarity(vectors)
print("✅ Similarity Matrix Created:", similarity.shape)


# --------------------------------------------------
# ✅ STEP 8 — SAVE MODEL FILES
# --------------------------------------------------

#pickle.dump(df, open("movies.pkl", "wb"))
#pickle.dump(similarity, open("similarity.pkl", "wb"))

#print("✅ MODEL FILES SAVED: movies.pkl & similarity.pkl")


# --------------------------------------------------
# ✅ STEP 9 — RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend(movie):
    movie = movie.lower()
    if movie not in df['title'].str.lower().values:
        print("❌ Movie not found in dataset")
        return

    index = df[df['title'].str.lower() == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print(f"\n✅ Top Recommendations for ✅ {df.iloc[index].title}:\n")
    for i in movie_list:
        print(df.iloc[i[0]].title)


# --------------------------------------------------
# ✅ TEST RECOMMENDATION
# --------------------------------------------------

# Example:
# recommend("Baahubali: The Beginning")
