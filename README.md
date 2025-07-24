# 🌡️ 서버실 온습도 모니터링 시스템

Raspberry Pi와 Flask를 기반으로 한 **서버실 온습도 실시간 감시 시스템**입니다.

## 개요
- 서버실 내부의 온도 및 습도를 실시간으로 모니터링
- 기준치를 벗어날 경우 LED 점등 및 부저 경고
- Flask 기반 웹 대시보드 제공

## 📌 주요 기능

- DHT11 센서로 온도/습도 측정 및 상태 판단 (6초 주기)
- 기준치 이상 시 LED(정상: 녹색, 이상: 빨간색) 색상 변경 및 부저 경고
- Flask 웹 대시보드에서 실시간 상태 확인 (비동기 fetch)
- MySQL DB에 모든 데이터 저장

## 🖼️ 시스템 구조
- 센서 → Raspberry Pi → DB 저장 → Flask → 웹 대시보드
            ↘ LED/Buzzer  
![시스템 다이어그램](./img/system-diagram2.png)


## 🧱 기술 스택

- Python 3.11.9 + Flask
- RPi.GPIO
- MySQL
- HTML/CSS + JavaScript (Fetch API)

## 📁 디렉토리 구조
```
project/
├── sensor_collector.py     # 센서 데이터 수집 + GPIO 제어
├── app.py                  # Flask 웹 서버 + API + 이메일 전송
├── config.py               # 임계값, SMTP, DB 설정
├── database.py             # MySQL 연결 및 쿼리 함수
├── send_email_alert.py     # 이메일 전송 함수
├── templates/index.html    # 대시보드 페이지
├── static/js/main.js       # 비동기 JS

```

## ⚙️ 실행 방법

1. 환경 설정
```bash
sudo apt install python3-pip
pip install flask pymysql
```

2. MySQL에 테이블 생성
```sql
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
```

4. 센서 수집 스크립트 실행
```bash
python3 sensor_collector.py
```

📊 미리보기
대시보드에서 현재 온도/습도 및 상태를 실시간 표시합니다.



1. 기능별 마일스톤
단계	기능	설명
1단계		환경 구성	Raspberry Pi 설정, Python 패키지 설치 (Flask, GPIO, pymysql 등)
2단계		센서 데이터 수집	DHT 센서값 주기적 수집, 기준치 이상이면 LED/Buzzer 제어
3단계	DB 연동	MySQL DB에 6초마다 온습도 값 및 상태 저장
4단계	웹 대시보드 기본	Flask 웹 서버 구축, HTML+JS로 실시간 데이터 표시
5단계	비동기 갱신	JavaScript fetch로 최신 온습도 상태 6초마다 업데이트
6단계	상태 색상 표시	정상: 초록 / 이상: 빨강 LED & 웹에서 시각적으로 표시
7단계	그래프 추가 (선택)	Chart.js 등을 활용해 과거 데이터 시각화
8단계	알림 기능 (선택)	이상 상태 시 이메일/텔레그램 알림 연동
9단계	최종 점검 및 배포	UI 정리, README 작성, github 

2. UI 설계 예시 (HTML 대시보드)
```pgsql
코드 복사
+----------------------------------------------------+
|           서버실 온습도 상태 모니터링              |
+----------------------------------------------------+
| 온도:   24.3°C           |   습도:  48.2%           |
| 상태:  ✅ 정상 (녹색)    |   측정 시간: 12:45:06    |
+----------------------------------------------------+
| [경고 LED] ●           [부저] OFF                  |
+----------------------------------------------------+
| [온도/습도 추이 그래프 영역]                       |
|  (Chart.js로 1시간 단위 표시)                      |
+----------------------------------------------------+
```
UI는 Bootstrap + JS 조합

측정값은 6초마다 fetch로 갱신

상태에 따라 배경/아이콘/글씨 색 변화

✅ 개요
서버실 내부의 온도 및 습도를 실시간으로 모니터링

기준치를 벗어날 경우 LED 점등 및 부저 경고

Flask 기반 웹 대시보드 제공

✅ 시스템 구성도
DHT11 → Raspberry Pi (GPIO) → DB 저장 → Flask 서버 → 웹 표시

✅ 주요 기능
6초 주기 센서 측정 및 상태 판단

LED (정상: 녹색, 이상: 빨간색), 부저 제어

MySQL DB에 로그 저장

웹 대시보드에서 실시간 확인 (비동기 fetch)

✅ 개발환경
Raspberry Pi 5

Python 3.x

Flask, RPi.GPIO

MySQL 8.x

JavaScript (fetch), HTML/CSS

✅ 개선 및 확장 가능성
상태 알림 (이메일, 텔레그램)

멀티 센서 / 구역 모니터링 (MQTT)

사용자 로그인 및 권한 관리

## 2일차
### DB 테이블 생성
- MariaDB 연결 시 비밀번호 오류 발생
  - mysqld_safe를 동시에 두 번 실행해버렸음(MariaDB 서버 충돌 나고 소켓 파일도 꼬임)

1. MariaDB 관련 프로세스 완전 종료
```bash
sudo pkill -9 mysqld
sudo pkill -9 mariadbd

# 프로세스 확인
ps aux | grep mysqld
# "grep --color=auto mysqld" 한 줄만 남으면 성공
```

2. 필요한 디렉토리 소유권 복구
```bash
sudo chown -R mysql:mysql /var/lib/mysql
sudo chown -R mysql:mysql /run/mysqld
```

3. 안전모드 실행(비밀번호 초기화용, 한 번만 실행)
```bash
sudo mysqld_safe --skip-grant-tables --skip-networking &
```

4. 다른 터미널 or 탭에서 mysql 접속 시도
```bash
sudo mysql -u root
```

5. 비밀번호 초기화
```bash
USE mysql;

# 암호 재설정
UPDATE mysql.global_priv 
SET priv = JSON_SET(priv, '$.authentication_string', PASSWORD('12345')) 
WHERE User = 'root';

FLUSH PRIVILEGES;
```

6. mysqld_safe 종료 및 서비스 재시작
```bash

sudo pkill -f mysqld
sudo systemctl start 
```

2. MariaDB 서버 정상 시작
```bash
ps aux | grep mysqld
```

3. root 계정으로 정상 접속 테스트
```bash
mysql -u root -p
# 암호입력
```

mysql 접속 후
```bash
CREATE DATABASE sensordata;
USE sensordata;

CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    led_state BOOLEAN DEFAULT FALSE,
    buzzer_state BOOLEAN DEFAULT FALSE
);
```
- Flask 서버
- JavaScript의 fetch() 함수와 setInterval()을 이용한 비동기 주기 폴링 방식
- 브라우저를 새로고침하지 않아도, 백엔드 API(/api/data)에서 데이터를 n초마다 자동으로 가져와 화면에 갱신하는 방식

```html
fetchData();                  // 페이지 처음 로딩 시 1회 실행
setInterval(fetchData, 5000); // 이후 5초마다 fetchData 반복 호출 (비동기 폴링)
```

### SMTP 메일 발송
- Gmail은 일반 계정 비밀번호로 SMTP 접속 막아둠 > 앱 비밀번호 발급 필요
  - https://myaccount.google.com/apppasswords
  - 16자리 코드 PASSWORD에 입력

### 개선점
1. 그래프 시각화
- Chart.js를 사용하여 온도/습도 데이터를 실시간 선 그래프로 표시
- 1초마다 /api/data 호출하여 새 데이터 반영

2. 부트스트랩 아이콘 추가
- 상단 제목 옆에 thermometer-half, droplet, clock 등의 아이콘 추가
- Bootstrap 5의 bootstrap-icons CDN 포함

3. 임계값 초과 시 강조 색상
- 온도 28도 초과 → 빨간색 (text-danger)
- 습도 60% 초과 → 파란색 강조 (text-primary fw-bold)
- 조건에 따라 CSS 클래스를 동적으로 변경

4. 메일 발송시 앱 멈춤 여부
- 메일 발송은 기본적으로 동기(synchronous) 처리되며, SMTP 응답이 느리면 전체 코드 흐름이 잠시 멈춤
- 해결 방법
  - 스레드(Thread)로 처리