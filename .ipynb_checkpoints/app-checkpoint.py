import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit.components.v1 import html

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

API_KEY = "e6a56cfdf62f1334a51c8f673756b2ac"

# ---------------------------------------------------------
# Custom CSS (UI Upgrade)
# ---------------------------------------------------------
st.markdown("""
<style>
/* Main Page Styling */
body {
    background-color: #0e1117;
    color: white;
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #FFDD57;
    margin-bottom: 15px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #d1d1d1;
    margin-bottom: 40px;
}

/* Movie Card */
.movie-card {
    background-color: #1a1c23;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
    border: 1px solid #333;
}

.movie-card:hover {
    transform: scale(1.05);
    border-color: #FFDD57;
}

/* Button Styling */
.stButton>button {
    background-color: #FFDD57;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 16px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #e6c74d;
}

/* Dropdown */
.stSelectbox div {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------
st.markdown('<h1 class="title">🎬 Tollywood Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find Similar Movies Instantly</p>', unsafe_allow_html=True)

movies_list = movies['title'].values

selected_movie = st.selectbox("Select a Movie to Recommend", movies_list)

# ---------------------------------------------------------
# Recommender Functions
# ---------------------------------------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url).json()
        poster_path = data["poster_path"]
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        return "https://via.placeholder.com/500x750.png?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750.png?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_idx = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []

    for idx, _ in movies_list_idx:
        movie_id = movies.iloc[idx].movie_id
        recommended_movies.append(movies.iloc[idx].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ---------------------------------------------------------
# Show Recommendations
# ---------------------------------------------------------
if st.button("🔍 Get Recommendations"):
    names, posters = recommend(selected_movie)

    st.write("")
    st.markdown("### Recommended Movies")
    st.write("")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" width="170" style="border-radius:10px;">
                    <p style="margin-top:10px; font-size:15px; color:#FFDD57;"><b>{names[i]}</b></p>
                </div>
            """, unsafe_allow_html=True)
