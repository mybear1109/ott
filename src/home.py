import streamlit as st
import src.movie_recommend as movie_recommend

def show_home_page():
    """홈 화면 표시"""
    st.markdown("<h2 class='sub-header'>🍿 오늘의 추천 영화</h2>", unsafe_allow_html=True)
    movies = movie_recommend.get_trending_movies()
    movie_recommend.display_movies(movies)
