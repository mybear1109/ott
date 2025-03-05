import requests
import streamlit as st
import webbrowser

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = st.secrets["MOVIEDB_API_KEY"]

# ---------------- 사용자 인증 및 프로필 관리 ----------------
def load_user_preferences():
    """📌 사용자의 선호 장르 및 설정을 로드합니다."""
    return st.session_state.get("user_profile", {})

def create_guest_session():
    """📌 TMDb에서 로그인 없이 영화 추천을 받을 수 있도록 게스트 세션 생성."""
    url = f"{BASE_URL}/authentication/guest_session/new?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data.get("success"):
        return data["guest_session_id"]
    else:
        print("게스트 세션 생성 실패:", data)
        return None

def show_login_form():
    """📌 로그인 폼을 표시하지만, 로그인 없이도 사용할 수 있도록 설정합니다."""
    st.title("🔑 로그인 (선택 사항)")
    st.write("TMDb 계정으로 로그인하거나, 로그인 없이 사용하세요.")
    username = st.text_input("사용자 이름 (선택 사항)")
    password = st.text_input("비밀번호 (선택 사항)", type="password")
    if st.button("로그인"): 
        st.session_state["SESSION_ID"] = username if username else "Guest"
        st.success(f"{username if username else 'Guest'}님, 환영합니다!")

def show_user_profile():
    """📌 사용자 프로필을 표시하지만, 로그인 없이도 기본적으로 사용 가능하도록 설정합니다."""
    st.sidebar.subheader("👤 사용자 프로필")
    username = st.session_state.get("SESSION_ID", "Guest")
    st.sidebar.write(f"**사용자:** {username}")
    if "SESSION_ID" in st.session_state and st.session_state["SESSION_ID"] != "Guest":
        if st.sidebar.button("로그아웃"):
            del st.session_state["SESSION_ID"]
            st.sidebar.success("로그아웃 되었습니다.")
