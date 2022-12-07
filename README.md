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
