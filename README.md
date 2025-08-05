# Starbucks Beverage Crawling Lambda API

이 프로젝트는 AWS Lambda를 이용하여 스타벅스 코리아 음료 데이터를 크롤링하고, JSON 형태로 반환하는 서버리스 API입니다.  
함수 URL을 호출하면 각 음료의 이름, 이미지, 종류, 온도, 영양 성분이 포함된 데이터를 가져올 수 있습니다.

## 📌 API 엔드포인트
- **Lambda Function URL**  
https://u6wvrcscqwe7rdbblr3xebajf40avfxz.lambda-url.ap-northeast-2.on.aws/

## 📦 응답 예시(JSON)
```json
[
{
  "name": "아메리카노",
  "image": "https://www.starbucks.co.kr/upload/store/skuimg/2023/09/[이미지경로]",
  "beverageType": "ESPRESSO",
  "beverageTemperature": "HOT",
  "beverageNutritions": {
    "TALL": {
      "servingKcal": 10,
      "saturatedFatG": 0,
      "proteinG": 1,
      "sodiumMg": 5,
      "sugarG": 0,
      "caffeineMg": 150
    }
  }
},
...
]
