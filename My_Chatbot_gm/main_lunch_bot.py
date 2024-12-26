# streamlit run C:\Users\user\Desktop\psh\project\My_Chatbot\main_lunch_bot.py
import streamlit as st
from lunch_bot import get_lunch_recommendations, find_restaurants_google
import folium
from streamlit_folium import st_folium

# 초기 상태 설정
if "restaurants" not in st.session_state:
    st.session_state["restaurants"] = []

if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = []

# Streamlit 앱 설정
st.set_page_config(page_title="Lunch AI Bot", page_icon="🤖🍽️", layout="wide")

st.title("Lunch AI Bot 🤖🍽️")
st.markdown("개인화된 점심 추천과 근처 맛집 정보를 제공합니다!")

# 사용자 입력
weather = st.text_input("오늘 날씨는 어떤가요?", placeholder="예: 춥고 비가 오는 날")
preference = st.selectbox("어떤 종류의 음식을 원하시나요?", ["매운 음식", "건강한 음식", "달달한 음식", "기름진 음식", "상관없음"])
mood = st.text_input("오늘 기분은 어떤가요?", placeholder="예: 피곤한 날, 활기찬 날")

# 점심 추천 버튼
if st.button("점심 추천 받기", key="recommend_button"):
    if weather and preference and mood:
        with st.spinner("추천을 찾고 있습니다..."):
            recommendations = get_lunch_recommendations(weather, preference, mood)
            st.session_state["recommendations"] = recommendations
        st.success("추천 결과를 확인하세요!")
    else:
        st.error("모든 입력란을 채워주세요!")

# 추천된 점심 옵션 표시
if st.session_state["recommendations"]:
    st.markdown("### 추천된 점심 옵션:")
    st.write(st.session_state["recommendations"])

# 사용자가 메뉴 선택 후 근처 맛집 검색
menu = st.text_input("추천받은 메뉴 중 마음에 드는 음식을 입력해주세요:", placeholder="예: 김치찌개")

# 근처 맛집 찾기 버튼
latitude, longitude = 37.5665, 126.9780  # 기본 좌표: 서울
if st.button("근처 맛집 찾기", key="find_restaurant_button"):
    if menu.strip():
        with st.spinner("맛집을 검색 중이에요..."):
            restaurants = find_restaurants_google(menu, latitude, longitude)
            st.session_state["restaurants"] = restaurants
            if restaurants:
                st.success(f"근처에서 {len(restaurants)}개의 맛집을 찾았어요!")
            else:
                st.error("맛집을 찾을 수 없어요. 다른 메뉴를 시도해보세요.")
    else:
        st.error("검색할 메뉴를 입력해주세요.")

# 검색된 맛집 표시
if st.session_state["restaurants"]:
    st.markdown("### 근처 맛집:")
    for i, restaurant in enumerate(st.session_state["restaurants"][:5], 1):
        st.write(f"{i}. {restaurant['name']} - {restaurant['distance']}m 거리")
        st.write(f"주소: {restaurant['address']}")

    # 지도 표시
    map_center = [latitude, longitude]
    m = folium.Map(location=map_center, zoom_start=15)
    for restaurant in st.session_state["restaurants"]:
        loc = restaurant["location"]
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=f"{restaurant['name']} ({restaurant['distance']}m)",
            tooltip=restaurant['name']
        ).add_to(m)
    st_folium(m, width=700, height=500)
