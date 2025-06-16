import requests
import json

# JS 파일 주소 목록 (카테고리별)
urls = {
    "W0000003": "ESPRESSO",
    "W0000171": "Cold_Brew",
    "W0000060": "Cold_Brew",
    "W0000004": "FRAPPUCCINO",
    "W0000005": "BLENDED",
    "W0000075": "TEA",
    "W0000422": "ANY",
    "W0000061": "ANY",
    "W0000053": "ANY",
    "W0000062": "ANY",
}

# 전체 결과 저장 리스트
result = []

# 크롤링 시작
for code, beverage_type in urls.items():
    url = f"https://www.starbucks.co.kr/upload/json/menu/{code}.js"
    print(f"Fetching: {url}")
    res = requests.get(url)
    text = res.text.replace("\ufeff", "")  # BOM 제거

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(f"JSON 파싱 실패: {url}")
        continue

    for item in data.get("list", []):
        result.append({
            "productCd": item.get("product_CD"),
            "name": item.get("product_NM"),
            "image": f"https://www.starbucks.co.kr{item.get('file_PATH', '')}",
            "beverageType": beverage_type,
            "beverageNutrition": {
                "servingKcal": item.get("kcal"),
                "saturatedFatG": item.get("sat_FAT"),
                "proteinG": item.get("protein"),
                "sodiumMg": item.get("sodium"),
                "sugarG": item.get("sugars"),
                "caffeineMg": item.get("caffeine")
            }
        })

# JSON 출력
print(json.dumps(result, indent=2, ensure_ascii=False))