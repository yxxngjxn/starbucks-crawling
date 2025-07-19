import re

def get_beverage_temperature(name: str, beverage_type: str) -> str:
    name = name.lower()

    # 조건 1. 이름에 'ML' 포함 → ICE/HOT 구분 없음
    if "ml" in name:
        return None

    # 조건 2. 특정 이름은 ICE/HOT 구분 없음
    neutral_names = [
        "시그니처 더 블랙 콜드 브루",
        "스타벅스 클래식 밀크 티 보틀"
    ]
    if name in [n.lower() for n in neutral_names]:
        return None
    
    # 조건 3. 특정 카테고리는 무조건 ICE
    if beverage_type in ["Cold_Brew", "FRAPPUCCINO", "BLENDED"]:
        return "ICE"

    # 조건 4. 이름에 '아이스', '피지오', '아포카토', '플라이트' 포함되면 ICE
    if any(keyword in name for keyword in ['아이스', '피지오', '아포카토', '플라이트']):
        return "ICE"
    
    # 조건 5. 특정 메뉴명은 무조건 ICE
    ice_names = [
        "스파클링 시트러스 에스프레소",
        "에스프레소 플라이트 도산",
        "스타벅스 망고 라떼"
        "딸기 콜드폼 초콜릿",
        "딸기 콜드폼 딸기 라떼",
        "스타벅스 슬래머",
        "우유",
        "제주팔삭 셔벗"
    ]
    if name in [n.lower() for n in ice_names]:
        return "ICE"

    # 조건 6. 나머지는 HOT
    return "HOT"

def normalize_name(name: str) -> str:
    return re.sub(r'\s+', '', name.lower().replace('스타벅스', '').replace(' ', ''))