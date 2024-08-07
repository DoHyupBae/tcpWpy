# 데이터 송수신 프로젝트
#### TCP 유니캐스트 방식의 실시간 수질 데이터 송수신 프로그램

---
## 목적
- 센서가 실시간으로 측정하는 데이터의 송수신 구현
- 데이터 전송 과정(TCP 프로토콜, 소켓 통신) 이해 및 직접 구현
- PostgreSQL 설치 및 DB 구축

---
## Stack
1. Python
2. PostgreSQL
3. TCP
4. Socket communication

---
## 구조
### 센서(Client)
- 센서를 통해 실시간으로 유량(flow), 오염물질1(impurities1), 오염물질2(impurities2), 시간(time)을 측정; 시간 이외 데이터는 랜덤으로 생성.
- 시간 데이터는 현장 측정 시간 기준 생성
- 본사와 연결 성공시 전송 시작(TCP)
- 1초 간격으로 측정 데이터 전송, 전송 성공시 해당 데이터 터미널에 출력
- client.py

### 본사 서버(Server)
- 소켓 생성 후 TCP 연결 성공시 데이터 수신
- 데이터 수신하여 DB에 입력
- server.py

### DB
- PostgreSQL 로 생성된 waterCondition의 realtime 테이블에 데이터 축적
- **columns** : flow, impurities1, impurities2, time

--- 
## 한계
1. 실제 센서를 통해 측정한 데이터가 아니므로 시각화 및 분석 무의미
2. 실제 센서를 통해 측정한 데이터가 아니므로 센서 연결시 일어날 수 있는 측정값
범위 등 오류 사전 방지 어려움
3. 공유기 내부 통신으로 외부 네트워크와 통신 구현되지 않음
4. PostgreSQL 등 툴 사용 미숙으로 시간 소모
5. 통신프로토콜에 대한 이해 부족으로 시간 소모

## 보완점
1. 실제 센서를 이용한 데이터 송수신 구현
2. 포트포워딩으로 현장 - 본사 통신 환경 구현
3. 포팅을 통한 속도 향상
4. 웹페이지, 대시보드 등을 이용한 데이터 시각화 수단 마련

---
## 구현 화면
### 서버 구동 터미널
![서버 터미널](https://github.com/user-attachments/assets/fe931f6b-3235-4b63-8f90-624ef6c36728)

### 클라이언트 구동 터미널
![클라이언트 터미널](https://github.com/user-attachments/assets/ffb3258f-373c-49eb-ad63-fabad639f639)

### DB 화면
![db 화면](https://github.com/user-attachments/assets/6e7960db-1ce1-44b2-8bf3-bc0bc888677a)

---
#### Updates
- 2024.08.07 server.py, client.py, db 완성
