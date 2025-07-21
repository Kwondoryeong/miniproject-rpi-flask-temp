# DB 연결 유틸
import pymysql

# 예시 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='youruser',
        password='yourpass',
        db='yourdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
