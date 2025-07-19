from app.crawling import get_crawled_data
from app.ocr import get_ocr_data
from app.utils import normalize_name
import unicodedata

def merge_beverage_data():
    crawled_data = get_crawled_data()
    ocr_data = get_ocr_data()

    for item in crawled_data:
        item["beverageNutritions"] = {
            k.upper(): v for k, v in item.get("beverageNutritions", {}).items()
        }

        normalized_name = normalize_name(item["name"])

        for ocr_item in ocr_data:
            ocr_name = normalize_name(ocr_item.get("name"))

            if normalized_name == ocr_name:
                nutrition = ocr_item.get("beverageNutrition")
                size = ocr_item.get("size", "").strip().upper()  # 대소문자, 공백 처리

                if nutrition and size != "TALL":
                    item["beverageNutritions"][size] = nutrition

    return crawled_data

if __name__ == "__main__":
    import json
    data = merge_beverage_data()