import streamlit as st
import src.ui as ui
import src.home as home
import src.auth_user as auth_user
import src.movie_recommend as movie_recommend

# ✅ 페이지 설정
st.set_page_config(page_title="MovieMind: 당신만의 영화 여정", page_icon="🎬", layout="wide")

def app():
    ui.load_css()
    ui.main_header()
    
    # ✅ 사용자 인증 및 로그인 여부 확인
    logged_in = ui.user_authentication()

    # ✅ 네비게이션 메뉴
    selected_page = ui.navigation_menu(logged_in)

    # ✅ 선택된 페이지에 따라 화면 변경
    if selected_page == "홈":
        home.show_home_page()
    elif selected_page == "즐겨찾기":
        ui.show_favorite_movies()
    elif selected_page == "영화 스타일 선택":
        ui.show_profile_setup()
    elif selected_page == "추천 생성":
        movie_recommend.show_generated_recommendations()

    ui.show_footer()

if __name__ == "__main__":
    app()
