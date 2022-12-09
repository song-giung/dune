# 요구사항

- docker-compose up 커맨드로 서비스를 띄운 후, 브라우져에서 http://localhost:8000/hello 를 호출하면, Hello ELECLE 1 텍스트가 출력된다.
- hello 가 호출된 시점으로부터 30초 동안, http://localhost:8000/hello/again 을 호출할 때 마다 동일한 메시지에서 “1” 부분만 1씩 증가되어 출력된다.
- hello 가 호출된 시점으로부터 30초가 경과된 이후부터는 hello/again 을 호출하면 Expired! 라는 메시지가 출력된다.
- Redis 와 Django 모두 Docker 를 통해서 run 되어야 한다.

## 실행

- docker compose up

## endpoint

- localhost:8000/hello
- localhost:8000/hello/again

---

## 후기

프리온보딩을 통해 알게 된 것

### Redis

- 인메모리 DB
- key, value 저장, 다양한 value 타입 존재
- key의 업데이트 : 한번 expired설정된 key에 대하여 직접 set등을 통해 업데이트가 불가능 하여 redis 내장 함수를 이용
  - [https://redis.io/commands/incr/](https://redis.io/commands/incr/)
  ```python
  class HelloAgainView(View):
      def get(self, request, *args, **kwargs):
          """후촐될 때 마다 유효한 캐쉬가 있을 경우 캐쉬의 값을 1 증가한 후 반환한다."""
          try:
              cache.incr(CACHE_KEY_HELLO)
              count = cache.get(CACHE_KEY_HELLO)
              # 캐쉬 키가 없을 경우 incr에서 ValueError 발생하여 따로 count의 유효성을 확인하지 않음
              return HttpResponse(get_text(count))
          except ValueError:
              return HttpResponse("Expired!")
  ```

### Docker

- 기본적인 Dockerfile 사용법 및 명령어

### Docker-compose

- 여러 컨테이너를 다루는 법
- 컨테이너 끼리의 통신

### Load balancer / Target group

- 트래픽 분산과 관리를 위한 LB
- LB의 대상이 되는 Target group

### ECS

- cluster, service, task 정의, task
  - 클러스터 > 여러개의 서비스 > 여러개의 태스크(컨테이너) 존재 가능
  - 그렇다면 서비스 간의 통신? 태스크 간의 통신은? 설정을 통해 가능하다.
  - Lauch type (Fargate, EC2)
    - Fargate
      - 사용한 만큼 비용 지불
      - EC2보다 세세한 설정이 불가능(예: GPU사용등이 필요할 경우 EC2사용 해야..)
    - EC2
      - 설정된 ec2 인스턴스 만큼 비용 지불
      - 모든 리소스를 사용하지 않더라도 풀 로드 기준으로 비용 부과
      - 인스턴스에 대한 좀 더 세세한 설정이 가능
- ECR 사용법
  - 생성된 이미지를 저장하고 aws cli등을 통해 저장된 이미지 사용 가능
- 커뮤니케이션
  - 서비스간 커뮤니케이션(AWS LB 설정 필요)
    ```python
    # 예를들어 django settings.py에서 redis 캐쉬 설정시
    # Cache setting
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://redis_cache:6379",  # docker container name
        }
    }

    ```
  - 동일한 task에 속한 컨테이너간 커뮤니케이션(AWS LB 설정 불필요 localhost로 접근 가능)
    ```python
    # 예를들어 django settings.py에서 redis 캐쉬 설정시
    # Cache setting
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://localhost:6379",
        }
    }

    ```

### 배포방식

- console
- cli
  - aws-cli
    - 다중 프로파일 사용법
  - ecs-cli
  - docker
    - docker context를 ecs로 변경하여 docker 명령어를 통해 ecs에 직접 배포할 수 있다. `docker compose up`
      - docker 명령어를 ecs에 반영하기 위해 context 생성 `docker context create ecs myecscontext`
      - 해당 context로 변경한 뒤 `docker context use myecscontext` ecs에 대한 제어를 docker 명령어로 실행 가능!
    - 장점 :
      - docker-compose파일을 읽어서 각 컨테이너 별로 서비스를 생성하여 자동으로 구성
      ```python
      x-aws-cluster: "dune"

      version: '3.7'
      services:
        web:
          image: "ECR IMAGE URI"
          ports:
            - 8000:8000
          command: python manage.py runserver 0.0.0.0:8000
          environment:
            DEBUG: 1
            PYTHONUNBUFFERED: 1
        redis_cache:
          image: "redis:alpine"
          ports:
            - 6379:6379
      ```
      - 위와 같이 설정 후 `docker compose up` 명령어를 실행할 경우 2개의 서비스(web, redis_cache), 로드밸런서, 타겟그룹 등을 `자동` 으로 생성해 준다.
    - 단점 :
      - 서비스 이름이라든지 일부 설정이 불가한 영역이 존재한다.
      - ecs 배포용 docker-compose 파일을 따로 작성해야 한다.

### 느낀점

- 인프라를 다루는데 있어 다양한 방식이 존재하는데, 어떠한 방식이 자동화에 있어서 제일 학습 곡선이 낮고 실무에 적응이 빠를까?
  1. 웹 콘솔(접근성이 제일 좋고 직관적)
  2. CLI(aws-cli, ecs-cli 등…)
  3. Copilot(대화형)
  4. CDK(인프라 리소스를 코드상으로 다룬다.)(가장 직관적이고 익숙한 언어로 접근이 가능해 보인다.)
- 인프라 설계 다중화, CI/CD 등 안정적인 서비스 운영을 위해서 공부할게 많다.

### 참고 자료

- [https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/Welcome.html](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/Welcome.html)
- [https://docs.docker.com/cloud/ecs-integration/](https://docs.docker.com/cloud/ecs-integration/)
- 기타 다양한 스택오버플로우…!!
