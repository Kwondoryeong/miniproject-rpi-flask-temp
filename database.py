# database.py

import mysql.connector
from config import DB_CONFIG

# DB 연결 함수
def get_connection():
    return mysql.connector.connect(**DB_CONFIG) #DB_CONFIG 사용

# 센서 데이터 삽입 함수
def insert_sensor_data(temperature, humidity, led_state, buzzer_state):
    conn = get_connection()
    cursor = conn.cursor()

    led_state = 0
    buzzer_state = 0
    sql = """
        INSERT INTO sensor_data (temperature, humidity, led_state, buzzer_state)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (temperature, humidity, led_state, buzzer_state))

    conn.commit()
    cursor.close()
    conn.close()

# 최신 센서 데이터 1개 가져오는 함수
def get_latest_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row

# 최근 1분간 로그 가져오는 함수
def get_recent_logs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    one_min_ago = datetime.now() - timedelta(minutes=1)
    query = """
        SELECT * FROM sensor_data
        WHERE created_at >= %s
        ORDER BY created_at DESC
    """
    cursor.execute(query, (one_min_ago,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
