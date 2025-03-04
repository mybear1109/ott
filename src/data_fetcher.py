import requests
import streamlit as st

API_KEY = st.secrets["MOVIEDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies_by_genre(genre_id):
    """장르별 영화 목록 가져오기"""
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=ko-KR"
    response = requests.get(url).json()
    return response.get("results", [])

def search_movie(query):
    """영화 검색"""
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}&language=ko-KR"
    response = requests.get(url).json()
    return response.get("results", [])
