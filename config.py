# DB 연결정보
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'sensordata',
    'port': 3306
}
# SMTP 메일발송
SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 587,
    "email": "smtptest3824@gmail.com",
    "password": "isizlfwtqexecsvk",
    "email_to": ["bazzi95@naver.com"]
#   "email_to": ["asdfgh@naver.com", "bestlife@naver.com"] #리스트로 여러 명 가능, 단일 ""
}
# 온습도 기준치 설정
SENSOR_CONFIG = {
    "TEMP_THRESHOLD": 27.0,
    "HUMIDITY_THRESHOLD": 50.0,
    "EMAIL_COOLDOWN_SECONDS": 300  # 5분
}
