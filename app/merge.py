# app/merge.py

from app.crawling import get_crawled_data
from app.ocr import get_ocr_data
from app.utils import normalize_name
import unicodedata

def merge_beverage_data():
    # 1. 크롤링 데이터와 OCR 데이터 가져오기
    crawled = get_crawled_data() # 크롤링한 모든 음료 (Tall 기준)
    ocr = get_ocr_data()         # 이미지에서 추출한 다른 사이즈들의 영양 성분

    # 2. 이름 기준으로 빠르게 찾기 위한 dict 만들기
    merged = {}
    for item in crawled:
        normalized_name = unicodedata.normalize("NFC", item["name"])
        merged[normalized_name] = item

    # 3. OCR 결과 병합하기
    for entry in ocr:
        name = unicodedata.normalize("NFC", entry.get("name"))
        size = entry.get("size")
        nutrition = entry.get("beverageNutrition")

        # 예외 처리) 이름이 크롤링 결과에 없으면 건너뜀
        if name not in merged:
            continue

        # 기존 객체에 사이즈별로 추가
        if "beverageNutritions" not in merged[name]:
            merged[name]["beverageNutritions"] = {}

        merged[name]["beverageNutritions"][size] = nutrition

    # 4. 병합 결과 리스트로 반환
    return list(merged.values())

if __name__ == "__main__":
    import json
    data = merge_beverage_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))