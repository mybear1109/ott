import streamlit as st
import src.data_fetcher as data_fetcher

def get_trending_movies():
    """트렌딩 영화 목록 가져오기"""
    return data_fetcher.fetch_movies_by_genre(28)  # 액션 장르 예시

def display_movies(movies):
    """영화를 5개씩 정렬하여 표시"""
    if not movies:
        st.warning("❌ 영화 정보를 불러오는 데 문제가 발생했습니다.")
        return
def get_full_poster_url(poster_path: str) -> str:
    """포스터 경로를 절대 URL로 변환"""
    if poster_path and not poster_path.startswith("http"):
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return poster_path or "https://via.placeholder.com/500x750?text=No+Image"
cols = st.columns(5)
for idx, movie in enumerate(movies[:5]):
    with cols[idx]:
        poster_url = get_full_poster_url(movie.get("poster_path"))
    st.image(poster_url, use_column_width=True)
    st.markdown(f"<p class='movie-title'>{movie.get('title', '제목 없음')}</p>", unsafe_allow_html=True)
