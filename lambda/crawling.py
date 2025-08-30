import requests
import json
from utils import get_beverage_temperature

def get_product_detail(product_cd):
    """개별 상품의 상세 정보를 AJAX API로 가져오기"""
    url = "https://www.starbucks.co.kr/menu/productViewAjax.do"
    data = {"product_cd": product_cd}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json().get("view", {})
    except Exception as e:
        print(f"상품 상세 정보 가져오기 실패 {product_cd}: {e}")
        return {}

def get_crawled_data():
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
    seen_beverages = set()  # 중복 제거용

    def safe_int(value):
        try:
            return int(value) if value else 0
        except (ValueError, TypeError):
            return 0

    # oz를 사이즈로 매핑
    size_mapping = {
        "8": "SHORT",    # 8oz = 237ml
        "12": "TALL",    # 12oz = 355ml  
        "16": "GRANDE",  # 16oz = 473ml
        "20": "VENTI",   # 20oz = 591ml
        "30": "TRENTA"   # 30oz = 887ml
    }

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
            name = item.get("product_NM")
            product_cd = item.get("product_CD")
            
            # 중복 체크 (동일한 음료명은 건너뛰기)
            if name in seen_beverages:
                continue
            seen_beverages.add(name)
            
            # 상세 정보 가져오기 (HOT/ICE 구분 및 정확한 사이즈)
            detail = get_product_detail(product_cd)
            if not detail:
                continue
                
            image_path = f"https://www.starbucks.co.kr{item.get('file_PATH', '')}"
            
            # HOT/ICE 구분
            hot_yn = detail.get("hot_YN", "Y")
            temperature = "HOT" if hot_yn == "Y" else "ICE"
            
            # 사이즈 정보 (상세 API에서 가져옴)
            standard_oz = str(detail.get("standard", "12"))
            actual_size = size_mapping.get(standard_oz, "TALL")
                    
            nutrition = {
                "servingKcal": safe_int(detail.get("kcal")),
                "saturatedFatG": safe_int(detail.get("sat_FAT")),
                "proteinG": safe_int(detail.get("protein")),
                "sodiumMg": safe_int(detail.get("sodium")),
                "sugarG": safe_int(detail.get("sugars")),
                "caffeineMg": safe_int(detail.get("caffeine"))
            }

            result.append({
                "name": name,
                "image": image_path,
                "beverageType": beverage_type,
                "beverageTemperature": temperature,  # API에서 가져온 정확한 온도
                "beverageNutritions": {
                    actual_size: nutrition  # API에서 가져온 정확한 사이즈
                }
            })

    return result