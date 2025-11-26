import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv("cleaned_dataset.csv")

# ✅ Reset index AFTER cleaning
df = df.reset_index(drop=True)

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

df['cast'] = df['cast'].apply(lambda x: x[:3] if x else [])

def get_director(crew_list):
    if not crew_list:
        return []
    return [person for person in crew_list if "director" in person.lower()][:1]

df['director'] = df['crew'].apply(get_director)

df['genres'] = df['genres'].apply(lambda x: " ".join(x))
df['cast'] = df['cast'].apply(lambda x: " ".join(x))
df['director'] = df['director'].apply(lambda x: " ".join(x))
df['overview'] = df['overview'].fillna("")

df['tags'] = (
    df['overview'] + " " +
    df['genres'] + " " +
    df['cast'] + " " +
    df['director']
)

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(df['tags']).toarray()

similarity = cosine_similarity(vectors)

# ✅ SAVE FILES AGAIN
pickle.dump(df, open("movies.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("✅ FIXED — Model rebuilt successfully!")
print("Movies shape:", df.shape)
print("Similarity shape:", similarity.shape)
