## 🚀 Spring Boot에서 AWS Lambda 호출 예시
#### 함수 URL : https://3x5wbokt4goucp6j5snlsfthla0bqmhx.lambda-url.ap-northeast-2.on.aws/
### 1. 의존성 추가 (Gradle 기준)
```
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
}
```
### 2. WebClient 코드 작성
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
