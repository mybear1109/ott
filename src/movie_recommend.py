import requests
import streamlit as st
from typing import List, Dict
from datetime import datetime

# ---------------- TMDb API 설정 ----------------
API_KEY = st.secrets["MOVIEDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

# ---------------- 트렌드 영화 가져오기 ----------------
def get_trending_movies() -> List[Dict]:
    """📌 주간 트렌딩 영화 목록을 가져옵니다."""
    url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 맞춤 추천 영화 가져오기 ----------------
def get_personalized_recommendations(user_profile: Dict) -> List[Dict]:
    """📌 사용자 프로필을 기반으로 맞춤 추천 영화를 가져옵니다."""
    preferred_genres = user_profile.get("preferred_genres", [])
    
    if not preferred_genres:
        return get_trending_movies()  # 기본적으로 트렌딩 영화 추천
    
    genre_ids = ",".join(map(str, preferred_genres))
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_ids}&language=ko-KR"
    
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 시간대 기반 추천 ----------------
def get_time_based_recommendations():
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
    
    return fetch_movies_by_genre(genre_id) if genre_id else get_trending_movies()

# ---------------- 장르 기반 추천 ----------------
def fetch_movies_by_genre(genre_id: int):
    """📌 특정 장르에 해당하는 영화 추천"""
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 인기 영화 추천 ----------------
def fetch_popular_movies():
    """📌 인기 영화 목록을 가져옵니다."""
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

# ---------------- 배우 기반 추천 ----------------
def search_person(name: str):
    """📌 배우 이름으로 TMDb에서 검색"""
    url = f"{BASE_URL}/search/person?api_key={API_KEY}&query={name}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []

def fetch_movies_by_person(person_id: int):
    """📌 특정 배우가 출연한 영화 목록 가져오기"""
    url = f"{BASE_URL}/person/{person_id}/movie_credits?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("cast", []) if response.status_code == 200 else []


### 무드(감정) 기반 영화 추천
def get_mood_based_recommendations(mood: str) -> List[Dict]:
    """
    사용자의 감정(무드)에 따라 추천 영화 목록을 가져옵니다.
    감정과 매핑된 장르 ID를 기반으로 영화를 필터링합니다.
    """
    url = f"{BASE_URL}/search/person?api_key={API_KEY}&query={mood}&language=ko-KR"
    response = requests.get(url)
    mood_to_genre = {
        "행복한": [35, 10751],  # 코미디, 가족
        "슬픈": [18, 10749],    # 드라마, 로맨스
        "신나는": [28, 12],     # 액션, 모험
        "로맨틱한": [10749, 35],# 로맨스, 코미디
        "무서운": [27, 53],     # 공포, 스릴러
        "미스터리한": [9648, 80],# 미스터리, 범죄
        "판타지한": [14, 12],   # 판타지, 모험
        "편안한": [99, 10770],   # 다큐멘터리, TV 영화
        "추억을 떠올리는": [10752, 36], # 전쟁, 역사
        "SF 같은": [878, 28]    # SF, 액션
    }
    return response.json().get("requests", []) if response.status_code == 200 else []

