import streamlit as st
import pickle
import time

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Page config
st.set_page_config(
    page_title="🎬 TFI Movie Recommender",
    layout="wide",
    page_icon="🎥",
)

# Dark + neon CSS
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
    }
    .stApp {
        background-color: #0d0d0d;
        color: #00eaff;
    }
    h1 {
        color: #00eaff !important;
        text-shadow: 0px 0px 15px #00eaff;
    }
    .movie-card {
        background: #1a1a1a;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 0 10px #00eaff55;
        text-align: center;
        color: #00eaff;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='text-align:center;'>
        🎬 TFI Movie Recommender
    </h1>
    <p style='text-align:center; color:#bbb; font-size:18px;'>
        Get smart Telugu movie recommendations instantly!
    </p>
""", unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("✨ Select a Movie", movie_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended = []
    for i in movie_list:
        recommended.append(movies.iloc[i[0]].title)
    return recommended

# Button
if st.button("🚀 Get Recommendations"):
    with st.spinner("🔎 Finding the best movies for you..."):
        time.sleep(1.5)  # Loading animation
        results = recommend(selected_movie)

    st.subheader("🌟 Top Recommendations")

    cols = st.columns(5)
    for i, movie in enumerate(results):
        with cols[i]:
            st.markdown(
                f"<div class='movie-card'>🎞️ {movie}</div>",
                unsafe_allow_html=True
            )

# Footer
st.markdown("""
    <hr style="border-color:#222;">
    <p style='text-align:center; color:#666;'>
        Made with ❤️ in dark mode
    </p>
""", unsafe_allow_html=True)
