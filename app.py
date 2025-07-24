from flask import Flask, render_template, jsonify, request
from database import get_latest_data, get_recent_logs, get_connection
from send_email_alert import send_alert
from config import SENSOR_CONFIG
import threading
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    data = get_latest_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({
            "temperature": None,
            "humidity": None,
            "created_at": None,
            "led_state": None,
            "buzzer_state": None
        })

@app.route("/api/logs")
def api_logs():
    try:
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

        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send-now", methods=["POST"])
def send_now():
    try:
        latest = get_latest_data()
        if not latest:
            return jsonify({"message": "📭 데이터가 없습니다."})

        temperature = latest["temperature"]
        humidity = latest["humidity"]

        subject = "📢 서버실 온습도 현황 보고"
        body = (
            "📦 현재 서버실 온습도 현황\n\n"
            f"🌡 온도: {temperature}°C\n"
            f"💧 습도: {humidity}%\n\n"
            "※ 이상징후가 발생할 경우 즉시 대응 바랍니다."
        )

        threading.Thread(target=send_alert, args=(subject, body)).start()
        return jsonify({"message": "✅ 이메일 발송 완료!"})
    except Exception as e:
        return jsonify({"message": f"⚠️ 오류 발생: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
