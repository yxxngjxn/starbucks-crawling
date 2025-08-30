from crawling import get_crawled_data
from utils import normalize_name
import os
import requests

def fetch_ocr_data(ocr_api_url: str) -> list[dict]:
    url = ocr_api_url.rstrip("/")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json()

def merge_beverage_data():
    ocr_api_url = os.getenv("OCR_API_URL")
    crawled_data = get_crawled_data()
    ocr_data = fetch_ocr_data(ocr_api_url)

    for item in crawled_data:
        # 기존 데이터 타입 통일 (모든 값을 int로 변환)
        normalized_nutrition = {}
        for size, nutrition in item.get("beverageNutritions", {}).items():
            normalized_nutrition[size.upper()] = {
                k: int(v) if str(v).isdigit() else 0 
                for k, v in nutrition.items()
            }
        item["beverageNutritions"] = normalized_nutrition

        normalized_name = normalize_name(item["name"])

        # OCR 데이터와 매칭
        for ocr_item in ocr_data:
            ocr_name = normalize_name(ocr_item.get("name"))

            if normalized_name == ocr_name:
                nutrition = ocr_item.get("beverageNutrition")
                size = ocr_item.get("size", "").strip().upper()

                # TALL이 아닌 사이즈만 OCR 데이터로 추가/업데이트
                if nutrition and size != "TALL":
                    # OCR 데이터는 이미 int 형태이므로 그대로 사용
                    item["beverageNutritions"][size] = nutrition

    return crawled_data

if __name__ == "__main__":
    import json
    data = merge_beverage_data()