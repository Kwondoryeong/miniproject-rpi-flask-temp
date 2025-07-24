import time
import adafruit_dht
import board
import RPi.GPIO as GPIO
import threading
from database import insert_sensor_data
from send_email_alert import send_alert # 이메일 알림
from config import SENSOR_CONFIG, SMTP_CONFIG

# DHT11 센서 설정 (GPIO26 = board.D26)
dht_sensor = adafruit_dht.DHT11(board.D6)

# LED GPIO 핀 설정
#LED_RED = 16
#LED_GREEN = 19

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(LED_RED, GPIO.OUT)
#GPIO.setup(LED_GREEN, GPIO.OUT)
#dht_sensor = adafruit_dht.DHT11(board.D6)

#GPIO.output(LED_RED, False)
#GPIO.output(LED_GREEN, True)

# CONFIG 사용으로 주석처리
# TEMP_THRESHOLD = 28.0
# HUMI_THRESHOLD = 60.0
temp_limit = SENSOR_CONFIG["TEMP_THRESHOLD"]
humi_limit = SENSOR_CONFIG["HUMIDITY_THRESHOLD"]
cooldown = SENSOR_CONFIG["EMAIL_COOLDOWN_SECONDS"]

# 마지막 메일 발송 시간 (기본값은 0)
last_sent_time = 0

while True:
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

        if temperature is not None and humidity is not None:
            led_state = 0  # 미사용
            buzzer_state = 0  # 미사용
            thflag = 0 # 1: 온습도, 2: 온도, 3: 습도
            print(f"🌡 Temp: {temperature}°C, 💧 Humidity: {humidity}%")
            insert_sensor_data(temperature, humidity, led_state, buzzer_state)

            # ✅ 메일 발송 조건 추가 (5분마다 한 번만)
            now = time.time()

            # LED 제어: 기준치 이하 -> 초록불, 이상 -> 빨간불
#            if temperature > temp_limit or humidity > humi_limit:
#                GPIO.output(LED_RED, True)
#                GPIO.output(LED_GREEN, False)
#            else:
#                GPIO.output(LED_RED, False)
#                GPIO.output(LED_GREEN, True)

            # 이메일 메시지 구성
            if( temperature > temp_limit and humidity > humi_limit ):
                thflag = 1
                email_msg = ("⚠️ 온습도 경고","온습도 기준치 초과입니다!!\n"
                          f"현재 온도: 🔥{temperature}°C\n"
                          f"현재 습도: 💧{humidity}%\n\n문의사항 있을 시 IT팀 권도형S 연락바랍니다.")

            elif (temperature > temp_limit):
                thflag = 2
                email_msg = ("⚠️ 온도 경고","온도 기준치 초과입니다!!\n"
                          f"현재 온도: 🔥{temperature}°C\n"
                          f"현재 습도: {humidity}%\n\n문의사항 있을 시 IT팀 권도형S 연락바랍니다.")
            elif(humidity > humi_limit):
                thflag = 3
                email_msg = ("⚠️ 습도 경고","습도 기준치 초과입니다!!\n"
                          f"현재 온도: {temperature}°C\n"
                          f"현재 습도: 💧{humidity}%\n\n문의사항 있을 시 IT팀 권도형S 연락바랍니다.")

            # 이메일 전송(5분에 1회 제한)
            if (thflag > 0) and (now - last_sent_time > cooldown):
                threading.Thread(
                    target=send_alert, args=email_msg
                ).start()
                last_sent_time = now


        else:
            print("⚠️ 센서에서 값을 읽을 수 없습니다.")

    except RuntimeError as e:
        print("⚠️ 센서 오류:", e.args[0])
        time.sleep(2)
        continue
    except KeyboardInterrupt:
        print("⛔ 종료합니다.")
        GPIO.cleanup()
        break
    finally:
        GPIO.cleanup()

    time.sleep(1)  # 1초마다 측정
