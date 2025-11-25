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

# ----------------------------------------------------------
# 🌟 CSS: Gradient Background + Search Bar Animation + Neon Glow
# ----------------------------------------------------------
st.markdown("""
    <style>

    /*  🌈 GRADIENT NEON BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #00111f, #001f3f, #29004e, #4b0055);
        background-size: 400% 400%;
        animation: gradientFlow 12s ease infinite;
        color: #00eaff;
    }

    @keyframes gradientFlow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* 🔥 TITLE */
    h1 {
        color: #00eaff !important;
        text-shadow: 0px 0px 25px #00eaff;
        font-weight: 800;
    }

    /* 🎞️ MOVIE CARD GLOW */
    .movie-card {
        background: rgba(10,10,20,0.7);
        padding: 15px;
        border-radius: 14px;
        border: 2px solid rgba(0,234,255,0.3);
        backdrop-filter: blur(6px);
        box-shadow: 0 0 15px #00eaff55;
        text-align: center;
        color: #00eaff;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.07);
        box-shadow: 0 0 25px #00eaff;
    }

    /* ✨ SEARCH BOX LABEL FIX */
    label, .stSelectbox label {
        color: #00eaff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        text-shadow: 0px 0px 8px #00eaff55;
    }

    /* ✨ ANIMATED SEARCH BOX */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.45) !important;
        color: #00eaff !important;
        border: 2px solid #00eaff55 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px #00eaff33;
        animation: pulseGlow 2.5s infinite;
    }

    .stSelectbox div[data-baseweb="select"] > div:hover {
        border-color: #00eaff;
        box-shadow: 0 0 25px #00eaff;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px #00eaff33; }
        50% { box-shadow: 0 0 20px #00eaff88; }
        100% { box-shadow: 0 0 10px #00eaff33; }
    }

    /* BUTTON NEON EFFECT */
    .stButton button {
        background: linear-gradient(90deg, #00eaff, #0088ff);
        color: black !important;
        border-radius: 10px;
        padding: 10px 25px;
        border: none;
        font-size: 16px;
        font-weight: 700;
        transition: 0.3s;
        box-shadow: 0 0 15px #00eaff;
    }

    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #00eaff;
    }

    /* FOOTER */
    .footer-text {
        color: #bbb !important;
        text-shadow: 0px 0px 5px #000;
    }

    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.markdown("""
    <h1 style='text-align:center;'>
        🎬 TFI Movie Recommender
    </h1>
    <p style='text-align:center; color:#d3d3d3; font-size:18px;'>
        Smart Telugu Movie Recommendations Powered by AI
    </p>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SEARCH BAR
# ----------------------------------------------------------
movie_list = movies['title'].values
selected_movie = st.selectbox("✨ Select a Movie", movie_list)

# ----------------------------------------------------------
# RECOMMENDATION FUNCTION
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# BUTTON + RESULTS
# ----------------------------------------------------------
if st.button("🚀 Get Recommendations"):
    with st.spinner("🔎 Finding movies..."):
        time.sleep(1.5)
        results = recommend(selected_movie)

    st.subheader("🌟 Top Recommendations")

    cols = st.columns(5)
    for i, movie in enumerate(results):
        with cols[i]:
            st.markdown(
                f"<div class='movie-card'>🎞️ {movie}</div>",
                unsafe_allow_html=True
            )

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------
st.markdown("""
    <br><hr style="border-color:#333;">
    <p class='footer-text' style='text-align:center;'>
        Made by <b>S. Bhanu Pavan Kalyan</b> 💙  
    </p>
""", unsafe_allow_html=True)
