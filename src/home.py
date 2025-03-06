import streamlit as st
import random
from src.movie_recommend import get_trending_movies, get_personalized_recommendations
from src.auth import load_user_preferences
from src.data_fetcher import get_movie_director_and_cast, fetch_movie_details

# ---------------- 전역 변수 ----------------
displayed_movie_ids = set()

# ---------------- 새로운 함수 추가 ----------------
def get_latest_popular_movies():
    return get_trending_movies()

def get_current_popular_movies():
    return get_trending_movies()

def get_realtime_popular_movies():
    return get_trending_movies()

def show_full_movie_details(movie):
    movie_id = movie.get("id")
    if not movie_id:
        st.write("상세 정보가 없습니다.")
        return
    
    details = fetch_movie_details(movie_id)
    if not details:
        st.write("상세 정보가 없습니다.")
        return
    
    title = details.get("title", "제목 없음")
    release_date = details.get("release_date", "정보 없음")
    vote_average = details.get("vote_average", "정보 없음")
    overview = details.get("overview", "줄거리 없음")
    
    # 감독 및 출연진 정보 가져오기
    credits = get_movie_director_and_cast(movie_id)
    directors = credits.get("directors", [])
    cast = credits.get("cast", [])
    
    st.markdown(f"### {title}")
    st.write(f"**개봉일:** {release_date}")
    st.write(f"**평점:** {vote_average}/10")
    st.write(f"**줄거리:** {overview}")
    if directors:
        st.write(f"**감독:** {', '.join(directors)}")
    if cast:
        st.write(f"**출연진:** {', '.join(cast[:10])}")

def show_movie_section(title, movies):
    st.markdown(f"<h2 class='sub-header'>{title}</h2>", unsafe_allow_html=True)
    
    if movies:
        selected_movies = random.sample(movies, min(5, len(movies)))
        cols = st.columns(5)

        for idx, movie in enumerate(selected_movies):
            with cols[idx]:
                poster_path = movie.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
                title = movie.get("title", "제목 없음")
                rating = movie.get("vote_average", "N/A")
                release_date = movie.get("release_date", "정보 없음")
                
                credits = get_movie_director_and_cast(movie.get("id", None))
                directors = credits.get("directors", [])
                cast = credits.get("cast", [])
                
                overview = movie.get("overview", "줄거리 없음")[:100] + "..."
                
                st.image(poster_url, width=250, use_container_width=False)
                st.markdown(f"""
                <div class='movie-card'>
                    <p class='movie-title'>{title}</p>
                    <p class='movie-info'>⭐ 평점: {rating}/10</p>
                    <p class='movie-info'>🗓 개봉일: {release_date}</p>
                    {f"<p class='movie-info'>🎬 감독: {', '.join(directors)}</p>" if directors else ''}
                    {f"<p class='movie-info'>👥 출연: {', '.join(cast[:3])}</p>" if cast else ''}
                    <p class='movie-info'>📜 줄거리: {overview}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("자세히 보기"):
                    show_full_movie_details(movie)
    else:
        st.warning(f"{title}를 불러오는 데 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def show_home_page():
    show_movie_section("🔝 트렌드 영화", get_trending_movies())
    show_movie_section("🚀 최신 인기 영화", get_latest_popular_movies())
    show_movie_section("🎥 현재 인기 영화", get_current_popular_movies())
    show_movie_section("📈 실시간 인기 영화", get_realtime_popular_movies())
    
    user_profile = load_user_preferences()
    recommended_movies = get_personalized_recommendations(user_profile) if user_profile else []
    show_movie_section("🍿 오늘의 추천 영화", recommended_movies)
