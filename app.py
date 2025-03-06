import streamlit as st
import src.auth
import src.ui
import src.home
import src.data_fetcher
import src.movie_recommend

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="MovieMind: 당신만의 영화 여정",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CSS 스타일 정의 ----------------
st.markdown("""
<style>
    .main-header {font-size: 3rem; font-weight: 700; color: #1DB954; text-align: center; margin-bottom: 2rem;}
    .sub-header {font-size: 2rem; font-weight: 600; color: #1DB954; margin-top: 2rem; margin-bottom: 1rem;}
    .movie-card {background-color: #282828; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;}
    .movie-title {font-size: 1.2rem; font-weight: 600; color: #FFFFFF;}
    .movie-info {font-size: 0.9rem; color: #B3B3B3;}
    .section-divider {margin-top: 2rem; margin-bottom: 2rem; border-top: 1px solid #333333;}
    .stButton>button {background-color: #1DB954; color: white;}
    .stButton>button:hover {background-color: #1ED760;}
    .button-container {display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)
# ---------------- 메인 헤더 출력 ----------------
def main_header():
    st.markdown("<h1 class='main-header'>MovieMind: 당신만의 영화 여정</h1>", unsafe_allow_html=True)

# ---------------- 상단 네비게이션 버튼 ----------------
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

if col1.button("🏠 홈"):
    st.session_state["selected_page"] = "홈"
elif col2.button("🎭 영화 스타일 선택"):
    st.session_state["selected_page"] = "영화 스타일 선택"
elif col3.button("🔍 영화 검색"):
    st.session_state["selected_page"] = "영화 검색"
elif col4.button("🎞 추천 생성"):
    st.session_state["selected_page"] = "추천 생성"

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 기본 화면 설정 ----------------
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "홈"

# ---------------- 선택한 페이지 실행 ----------------
if st.session_state["selected_page"] == "홈":
    src.home.show_home_page()
elif st.session_state["selected_page"] == "영화 스타일 선택":
    src.ui.show_profile_setup()
elif st.session_state["selected_page"] == "영화 검색":
    src.ui.show_movie_search()
elif st.session_state["selected_page"] == "추천 생성":
    src.ui.show_generated_recommendations()

# ---------------- 푸터 ----------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #B3B3B3; padding: 1rem;'>
        <p>© 2025 MovieMind. All rights reserved.</p>
        <p>Developed by <a href="https://github.com/mybear1109" style="color: #9A2EFE; text-decoration: none;">mybear1109 😻</a></p>
    </div>
    """,
    unsafe_allow_html=True
)