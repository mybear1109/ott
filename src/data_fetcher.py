import requests
import streamlit as st
from typing import List, Dict
from datetime import datetime
from deep_translator import GoogleTranslator

# ---------------- TMDb API 설정 ----------------
API_KEY = st.secrets["MOVIEDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# ---------------- 번역 기능 ----------------
def translate_text(text: str, source_lang: str = "auto", target_lang: str = "ko") -> str:
    """📌 Google Translator를 사용하여 텍스트 번역"""
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        print(f"번역 오류: {e}")
        return text  # 번역 실패 시 원본 반환
    
def translate_text(text: str, target_lang: str = "ko") -> str:
    """📌 Google Translate API를 직접 호출하여 텍스트 번역"""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",  # 원본 언어 자동 감지
        "tl": target_lang,
        "dt": "t",
        "q": text,
    }
    
    try:
        response = requests.get(url, params=params)
        translated_text = response.json()[0][0][0]
        return translated_text
    except Exception as e:
        print(f"번역 오류: {e}")
        return text  # 번역 실패 시 원본 반환    

# ---------------- 영화 번역 ----------------
def fetch_movie_translations(movie_id):
    """ 특정 영화의 한국어 번역 데이터 가져오기 """
    url = f"{BASE_URL}/movie/{movie_id}/translations?api_key={API_KEY}"
    try:
        response = requests.get(url)
        translations = response.json().get("translations", []) if response.status_code == 200 else []
        for t in translations:
            if t["iso_639_1"] == "ko":  # 한국어 데이터 찾기
                return t["data"].get("title", ""), t["data"].get("overview", "")
    except Exception as e:
        print(f"Error fetching movie translations: {e}")
    return None, None  # 번역 데이터가 없을 경우

def translate_movie(movie):
    """ 영화 정보를 한국어로 변환 (번역이 없을 경우 원본 유지) """
    title_ko, overview_ko = fetch_movie_translations(movie.get("id", 0))
    if title_ko:
        movie["title"] = title_ko
    if overview_ko:
        movie["overview"] = overview_ko
    
    # 감독 및 출연진 번역
    movie["directors"] = [translate_text(director) for director in movie.get("directors", [])]
    movie["cast"] = [translate_text(actor) for actor in movie.get("cast", [])]
    
    return movie

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
    """📌 특정 영화의 감독 및 출연진 정보를 가져와 한국어로 변환"""
    movie_details = fetch_movie_details(movie_id)
    credits = movie_details.get("credits", {})
    
    directors = [translate_text(member["name"]) for member in credits.get("crew", []) if member.get("job") == "Director"]
    cast = [translate_text(member["name"]) for member in credits.get("cast", [])]
    
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

# ---------------- 키워드 관련 함수 ----------------
def search_keyword_movies(query):
    """키워드로 영화를 검색합니다."""
    url = f"{BASE_URL}/search/keyword?api_key={API_KEY}&query={query}"
    try:
        response = requests.get(url)
        return response.json().get("results", []) if response.status_code == 200 else []
    except Exception as e:
        print(f"Error searching for keyword: {e}")
        return []

def fetch_movies_by_keyword(keyword_id):
    """특정 키워드에 해당하는 영화 목록을 가져옵니다."""
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_keywords={keyword_id}&language=ko-KR"
    try:
        response = requests.get(url)
        movies = response.json().get("results", []) if response.status_code == 200 else []
        return [translate_movie(movie) for movie in movies]
    except Exception as e:
        print(f"Error fetching movies by keyword: {e}")
        return []

def fetch_similar_movies(movie_id, page=1, language="ko-KR"):
    """
    특정 영화와 유사한 영화 목록을 가져옵니다.
    """
    url = f"{BASE_URL}/movie/{movie_id}/similar"
    params = {
        "api_key": API_KEY,
        "language": language,
        "page": page
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        return []
    except Exception as e:
        print(f"Error fetching similar movies: {e}")
        return []
    