import requests
import streamlit as st

API_KEY = st.secrets["MOVIEDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

def create_session():
    """사용자 세션 생성 (로그인)"""
    url = f"{BASE_URL}/authentication/token/new?api_key={API_KEY}"
    response = requests.get(url).json()
    request_token = response.get("request_token")

    if not request_token:
        return None

    auth_url = f"https://www.themoviedb.org/authenticate/{request_token}"
    st.write(f"🔗 [여기 클릭하여 승인하기]({auth_url})")

    session_url = f"{BASE_URL}/authentication/session/new?api_key={API_KEY}"
    session_response = requests.post(session_url, json={"request_token": request_token}).json()

    return session_response.get("session_id")

def create_guest_session():
    """게스트 모드 세션 생성"""
    url = f"{BASE_URL}/authentication/guest_session/new?api_key={API_KEY}"
    response = requests.get(url).json()
    return response.get("guest_session_id")

def delete_session():
    """사용자 세션 삭제 (로그아웃)"""
    if "SESSION_ID" in st.session_state:
        del st.session_state["SESSION_ID"]
        st.success("🚪 로그아웃 완료!")
        st.experimental_rerun()
    else:
        st.warning("⚠ 현재 로그인되어 있지 않습니다.")

def is_user_authenticated():
    """사용자 로그인 상태 확인"""
    return "SESSION_ID" in st.session_state
