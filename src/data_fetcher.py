import requests
import streamlit as st
from typing import List, Dict
from datetime import datetime

# ---------------- TMDb API 설정 ----------------
API_KEY = st.secrets["MOVIEDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# ---------------- 영화 검색 ----------------
def search_movie(query: str) -> List[Dict]:
    """📌 영화 제목으로 TMDb에서 검색"""
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 장르별 영화 가져오기 ----------------
def fetch_movies_by_genre(genre_id: int) -> List[Dict]:
    """📌 특정 장르에 해당하는 영화 추천"""
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 영화 세부 정보 가져오기 ----------------
def fetch_movie_details(movie_id: int) -> Dict:
    """📌 특정 영화의 세부 정보를 가져옴"""
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=ko-KR&append_to_response=credits"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

# ---------------- 감독 및 출연진 정보 가져오기 ----------------
def get_movie_director_and_cast(movie_id: int) -> Dict:
    """📌 특정 영화의 감독 및 출연진 정보를 가져옴"""
    movie_details = fetch_movie_details(movie_id)
    credits = movie_details.get("credits", {})
    
    directors = [member["name"] for member in credits.get("crew", []) if member.get("job") == "Director"]
    cast = [member["name"] for member in credits.get("cast", [])]
    
    return {"directors": directors, "cast": cast}

# ---------------- 시간대 기반 추천 ----------------
def get_time_based_recommendations() -> List[Dict]:
    """📌 현재 시간대에 따라 영화 추천"""
    current_hour = datetime.now().hour
    
    if 18 <= current_hour <= 23:
        genre_id = 18  # 드라마
    elif 7 <= current_hour <= 9 or 17 <= current_hour <= 19:
        genre_id = 35  # 코미디
    elif 0 <= current_hour <= 3:
        genre_id = 27  # 공포
    else:
        genre_id = None
    
    return fetch_movies_by_genre(genre_id) if genre_id else []

# ---------------- 날씨 기반 추천 ----------------
def get_weather_based_recommendations(city: str) -> List[Dict]:
    """📌 사용자의 지역 날씨를 기반으로 적절한 영화를 추천"""
    if not WEATHER_API_KEY:
        return []
    
    weather_response = requests.get(f"{WEATHER_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric")
    if weather_response.status_code != 200:
        return []
    
    weather = weather_response.json().get("weather", [{}])[0].get("main", "Clear")
    if weather in ["Rain", "Drizzle", "Thunderstorm"]:
        genre_id = "18,10749"  # 드라마, 로맨스
    else:
        genre_id = "35,28"  # 코미디, 액션
    
    return fetch_movies_by_genre(genre_id)