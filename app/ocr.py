import pytesseract
from PIL import Image
import os
import re
import json

def get_ocr_data():
    # 이미지가 저장된 폴더 경로
    image_dir = './image'
    ocr_results = []
    number_pattern = r'\d+(?:\.\d+)?'

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 확장자 제거
            filename_no_ext = os.path.splitext(filename)[0]  # 예: '스타벅스 꿀 호떡 라떼 GRANDE'
            name_parts = filename_no_ext.rsplit(' ', 1)

            if len(name_parts) != 2:
                continue

            beverage_name, size = name_parts
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path)

            # OCR
            text = pytesseract.image_to_string(image, lang='kor+eng')
            values = re.findall(number_pattern, text)

            if len(values) >= 6:
                nutrition = {
                    "servingKcal": float(values[0]),
                    "saturatedFatG": float(values[1]),
                    "proteinG": float(values[2]),
                    "sodiumMg": float(values[3]),
                    "sugarG": float(values[4]),
                    "caffeineMg": float(values[5])
                }
            else:
                nutrition = {}

            ocr_results.append({
                "name": beverage_name.strip(),
                "size": size.strip(),
                "beverageNutrition": nutrition
            })
    
    return ocr_results