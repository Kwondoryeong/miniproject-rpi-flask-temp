# 🌡️ 서버실 온습도 모니터링 시스템

Raspberry Pi와 Flask를 기반으로 한 **서버실 온습도 실시간 감시 시스템**입니다.

## 📌 주요 기능

- DHT11 센서로 온도/습도 측정 (6초마다)
- 기준치 이상 시 LED 색상 변경 및 부저 경고
- Flask 웹 대시보드에서 상태 확인 (비동기 갱신)
- MySQL DB에 모든 데이터 저장

## 🖼️ 시스템 구조
센서 → Raspberry Pi → DB 저장 → Flask → 웹 대시보드
↘ LED/Buzzer 


## 🧱 기술 스택

- Python 3.x + Flask
- RPi.GPIO
- MySQL
- HTML/CSS + JavaScript (Fetch API)

## 📁 디렉토리 구조
project/
├── app.py # Flask 서버
├── sensor_collector.py # 센서 수집 및 GPIO 제어
├── config.py # 기준 온도/습도 설정
├── database.py # DB 연결 유틸
├── templates/index.html # 대시보드
├── static/js/main.js # 비동기 fetch
└── README.md


## ⚙️ 실행 방법

1. 환경 설정
```bash
sudo apt install python3-pip
pip install flask pymysql

2.MySQL에 테이블 생성
```
sql
CREATE TABLE sensor_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  temperature FLOAT,
  humidity FLOAT,
  status ENUM('NORMAL','ALERT'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
3. Flask 서버 실행
```bash
python3 app.py
센서 수집 스크립트 실행
```
```bash
python3 sensor_collector.py
```
📊 미리보기
대시보드에서 현재 온도/습도 및 상태를 실시간 표시합니다.

