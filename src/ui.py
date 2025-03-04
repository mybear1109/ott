import streamlit as st
import src.auth_user as auth_user

def load_css():
    """CSS 로드"""
    st.markdown("""
    <style>
        .main-header { font-size: 3rem; font-weight: 700; text-align: center; }
        .sub-header { font-size: 2rem; font-weight: 600; margin-top: 2rem; }
        .movie-card { background-color: #282828; border-radius: 10px; padding: 1rem; }
        .movie-title { font-size: 1.2rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

def main_header():
    """메인 헤더"""
    st.markdown("<h1 class='main-header'>MovieMind: 당신만의 영화 여정</h1>", unsafe_allow_html=True)

def user_authentication():
    """사용자 로그인/로그아웃 처리"""
    session_active = auth_user.is_user_authenticated()
    if not session_active:
        if st.button("🔑 로그인"):
            session_id = auth_user.create_session()
            if session_id:
                st.session_state["SESSION_ID"] = session_id
                st.success("✅ 로그인 성공!")
                st.experimental_rerun()
    else:
        if st.button("🚪 로그아웃"):
            auth_user.delete_session()

def navigation_menu(logged_in):
    """네비게이션 메뉴"""
    return "홈"

def show_footer():
    """푸터"""
    st.markdown("<p style='text-align: center;'>© 2025 MovieMind.</p>", unsafe_allow_html=True)
