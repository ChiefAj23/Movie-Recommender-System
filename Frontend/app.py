import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ee18e826b20a63ab54fdf254ec1f0bf9&language=en-US'
    )
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in recommended_indices:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

movies_list = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
<style>
    .stButton > button {
        color: #FFFFFF !important;
        background-color: #FF4B4B;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #FF3030;
    }
    .stButton > button:active {
        background-color: #E00000;
        color: #FFFFFF !important;
    }
    .css-2trqyj, .stSelectbox div[role="combobox"] {
        font-size: 16px;
        padding: 8px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #888;'>Developed by Abhijeet Solanki</h4>", unsafe_allow_html=True)
st.markdown("---")
selected_movie_name = st.selectbox('🎥 Select your favorite movie:', movies['title'].values)

if st.button('Show Recommendations 🚀'):
    with st.spinner('🍿 Loading your recommendations...'):
        names, posters = recommend(selected_movie_name)

    st.markdown("---")
    columns = st.columns(5)

    for col, name, poster in zip(columns, names, posters):
        with col:
            st.markdown(f"#### {name}")
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown("<div style='text-align: center; color: #CCC;'>Poster not available 😕</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #AAA; padding-top: 30px;'>© 2025 Abhijeet Solanki. All rights reserved.</div>", unsafe_allow_html=True)
