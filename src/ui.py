import streamlit as st
from src.movie_recommend import get_trending_movies, get_personalized_recommendations
from src.data_fetcher import search_movie, fetch_movies_by_genre
from src.auth import load_user_preferences

# ---------------- 영화 스타일 설정 ----------------
def show_profile_setup():
    """ 사용자 영화 취향 설정 """
    st.title("🎬 영화 스타일 설정")
    st.write("사용자의 선호 장르를 선택하세요.")
    
    genre_map = {"액션": 28, "코미디": 35, "드라마": 18, "공포": 27, "SF": 878}
    selected_genres = st.multiselect("선호하는 장르를 선택하세요", list(genre_map.keys()))
    
    if st.button("저장"): 
        user_profile = {"preferred_genres": [genre_map[genre] for genre in selected_genres]}
        st.session_state["user_profile"] = user_profile
        st.success("선호 장르가 저장되었습니다!")

# ---------------- 영화 검색 ----------------
def show_movie_search():
    """ 영화 검색 기능 """
    st.title("🔍 영화 검색")
    search_query = st.text_input("영화 제목을 입력하세요")
    
    if st.button("검색") and search_query:
        results = search_movie(search_query)
        if results:
            for movie in results[:5]:
                st.write(f"🎥 {movie['title']} ({movie.get('release_date', 'Unknown')[:4]})")
                st.image(f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}", width=150)
        else:
            st.warning("검색된 영화가 없습니다.")

# ---------------- 즐겨찾기 ----------------
def show_favorite_movies():
    """ 사용자가 즐겨찾기에 추가한 영화 표시 """
    st.title("🌟 즐겨찾기 영화")
    st.write("현재 즐겨찾기에 추가된 영화가 없습니다.")

# ---------------- 추천 생성 ----------------
def show_generated_recommendations():
    """ 맞춤 추천 영화 생성 """
    st.title("🎞️ 맞춤 영화 추천")
    user_profile = st.session_state.get("user_profile", load_user_preferences())
    
    if user_profile:
        movies = get_personalized_recommendations(user_profile)
        if movies:
            for movie in movies[:5]:
                st.write(f"🎥 {movie['title']} ({movie.get('release_date', 'Unknown')[:4]})")
                st.image(f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}", width=150)
        else:
            st.warning("추천할 영화가 없습니다.")
    else:
        st.warning("사용자 프로필이 설정되지 않았습니다. 영화 스타일을 먼저 설정해주세요.")