## 🚀 Spring Boot에서 AWS Lambda 호출 예시
#### 함수 URL : https://3x5wbokt4goucp6j5snlsfthla0bqmhx.lambda-url.ap-northeast-2.on.aws/
#### 함수 URL 2 : https://dla6sbxferlsb2jl6wtmjvmioe0hdmdc.lambda-url.ap-northeast-2.on.aws/
(AWS 계정에 약간의 문제가 생겨서 첫 번째 주소가 제대로 안 되면 두 번째 주소 사용해 주세요!)
### 1. 의존성 추가 (Gradle 기준)
```
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
}
```
### 2. 컨트롤러 작성
```
package com.example.lambdatest;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@RestController
public class TestController {

    private final WebClient webClient = WebClient.create();

    @GetMapping("/test-lambda")
    public Mono<String> callLambda() {
        return webClient.get()
                .uri("https://3x5wbokt4goucp6j5snlsfthla0bqmhx.lambda-url.ap-northeast-2.on.aws/")
                .retrieve()
                .bodyToMono(String.class);
    }

}
```
### 3. 실행 방법
### 3-1. Spring Boot 서버 실행
```
./gradlew bootRun
```
### 3-2. 브라우저 또는 API 도구(Postman 등)에서 아래 주소로 GET 요청
```
http://localhost:8080/test-lambda
```

<br/>

## 📦 Lambda 응답 JSON 구조
### 1. 구조 설명
| 필드명                 | 타입     | 설명                                     |
| ------------------- | ------ | -------------------------------------- |
| `name`              | String | 음료 이름 (예: "에스프레소", "콜드 브루")            |
| `image`             | String | 음료 이미지 URL (스타벅스 공식 이미지 주소)            |
| `beverageType`      | String | 음료 분류 (예: ESPRESSO, Cold\_Brew, TEA 등) |
| `beverageNutrition` | Object | 영양 정보가 담긴 객체                           |
| ├ `servingKcal`     | String | 1회 제공량당 열량 (kcal)                      |
| ├ `saturatedFatG`   | String | 포화지방 (g)                               |
| ├ `proteinG`        | String | 단백질 (g)                                |
| ├ `sodiumMg`        | String | 나트륨 (mg)                               |
| ├ `sugarG`          | String | 당류 (g)                                 |
| └ `caffeineMg`      | String | 카페인 (mg)                               |
### 2. 예시 (부분 발췌)
```
[
  {
    "name": "에스프레소",
    "image": "https://www.starbucks.co.kr/upload/store/2023/10/[...]",
    "beverageType": "ESPRESSO",
    "beverageNutrition": {
      "servingKcal": "15",
      "saturatedFatG": "0.1",
      "proteinG": "0.8",
      "sodiumMg": "0",
      "sugarG": "0",
      "caffeineMg": "75"
    }
  },
  {
    "name": "콜드 브루",
    "image": "https://www.starbucks.co.kr/upload/store/2023/09/[...]",
    "beverageType": "Cold_Brew",
    "beverageNutrition": {
      "servingKcal": "5",
      "saturatedFatG": "0",
      "proteinG": "0",
      "sodiumMg": "0",
      "sugarG": "0",
      "caffeineMg": "150"
    }
  }
  ...
]
```
