
import requests
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("google_api_key")
# GPT 모델을 사용한 점심 추천
def get_lunch_recommendations(weather, preference, mood):
    prompt = (
        f"날씨가 {weather}입니다. 사용자는 {preference} 음식을 선호하며 기분은 {mood}입니다. "
        "이 조건에 따라 한국 음식을 중심으로 3가지 점심 메뉴를 추천해 주세요. 각 메뉴에 대한 간단한 설명도 포함해주세요."
    )
    try:
        response = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "당신은 한국 음식을 추천하는 유용한 AI 비서입니다."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
            temperature=0.7,
            max_tokens=300
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 음식 사진 검색 
def get_food_image(food_name):
    """
    Unsplash API를 사용하여 음식 사진 검색.
    """
    unsplash_api_key = "your-unsplash-api-key"
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": food_name,
        "client_id": unsplash_api_key,
        "per_page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]["urls"]["regular"]
    return None




from math import radians, cos, sin, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    두 지점 간의 거리를 계산 (단위: 미터)
    """
    R = 6371000  # 지구 반지름 (미터)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_restaurants_google(keyword, latitude, longitude):
    """
    Google Places API를 사용하여 음식점 검색 및 거리 계산.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": google_api_key,
        "location": f"{latitude},{longitude}",
        "radius": 3000,  # 검색 반경 (단위: 미터)
        "keyword": keyword,
        "type": "restaurant",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        restaurants = []
        for place in results:
            place_location = place.get("geometry", {}).get("location", {})
            if place_location:
                lat2 = place_location.get("lat")
                lon2 = place_location.get("lng")
                distance = calculate_distance(latitude, longitude, lat2, lon2)
                restaurant = {
                    "name": place.get("name"),
                    "address": place.get("vicinity"),
                    "rating": place.get("rating", "No rating"),
                    "location": place_location,
                    "distance": round(distance),  # 거리 (미터) 추가
                }
                restaurants.append(restaurant)
        return restaurants
    else:
        print(f"Google API 호출 실패: {response.status_code}")
        print("응답 내용:", response.text)
        return []
    
