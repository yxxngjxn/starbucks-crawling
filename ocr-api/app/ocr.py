import pytesseract
from PIL import Image
import os
import re
import json

def extract_nutrition_from_text(text):
    nutrition = {}
    
    # 단위별 숫자 추출
    kcal_match = re.search(r'(\d+)kcal', text)
    g_values = re.findall(r'(\d+)g', text)
    mg_values = re.findall(r'(\d+)mg', text)
    
    # 칼로리 추출
    if kcal_match:
        nutrition['servingKcal'] = int(kcal_match.group(1))
    
    # g 단위 값들 (탄수화물, 당류, 단백질 순서로 가정)
    if len(g_values) >= 3:
        nutrition['saturatedFatG'] = int(g_values[0])
        nutrition['sugarG'] = int(g_values[1])
        nutrition['proteinG'] = int(g_values[2])
    elif len(g_values) >= 2:
        nutrition['saturatedFatG'] = int(g_values[0])  
        nutrition['sugarG'] = int(g_values[1])
        nutrition['proteinG'] = 0
    
    # mg 단위 값들 (나트륨, 카페인)
    if len(mg_values) >= 2:
        nutrition['sodiumMg'] = int(mg_values[0])
        nutrition['caffeineMg'] = int(mg_values[-1])
    elif len(mg_values) >= 1:
        # 하나만 있으면 나트륨으로 가정 (카페인은 0)
        nutrition['sodiumMg'] = int(mg_values[0])
        nutrition['caffeineMg'] = 0
    
    # 필수 필드 기본값 설정
    required_keys = ['servingKcal', 'saturatedFatG', 'proteinG', 'sodiumMg', 'sugarG', 'caffeineMg']
    for key in required_keys:
        if key not in nutrition:
            nutrition[key] = 0
            
    # 최소한 칼로리가 있어야 유효한 데이터로 간주
    if nutrition.get('servingKcal', 0) == 0:
        return {}
            
    return nutrition

def get_ocr_data():
    # 이미지가 저장된 폴더 경로
    image_dir = './image'
    ocr_results = []
    seen_combinations = set()
    number_pattern = r'\d+(?:\.\d+)?'

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 확장자 제거
            filename_no_ext = os.path.splitext(filename)[0]
            
            # .PNG가 중복으로 있는 경우 추가 제거
            if filename_no_ext.upper().endswith('.PNG'):
                filename_no_ext = filename_no_ext[:-4]
            
            name_parts = filename_no_ext.rsplit(' ', 1)

            if len(name_parts) != 2:
                continue

            beverage_name, size = name_parts
            
            # 중복 제거를 위한 키 생성
            combination_key = (beverage_name.strip().lower(), size.strip().upper())
            if combination_key in seen_combinations:
                continue
            seen_combinations.add(combination_key)
            
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path)

            # OCR
            text = pytesseract.image_to_string(image, lang='kor+eng')
            
            
            # 라벨 기반 영양성분 추출
            nutrition = extract_nutrition_from_text(text)

            ocr_results.append({
                "name": beverage_name.strip(),
                "size": size.strip(),
                "beverageNutrition": nutrition
            })
    
    return ocr_results

if __name__ == "__main__":
    result = get_ocr_data()
    print(f"Total results: {len(result)}")