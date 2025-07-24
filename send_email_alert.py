import smtplib
from email.mime.text import MIMEText
from config import SMTP_CONFIG

def send_alert(subject, message):
    # 수신자 리스트 → 문자열로 연결
    recipients = SMTP_CONFIG["email_to"] if isinstance(SMTP_CONFIG["email_to"], list) else [SMTP_CONFIG["email_to"]]

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SMTP_CONFIG["email"]
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_CONFIG["server"], SMTP_CONFIG["port"]) as server:
            server.starttls()
            server.login(SMTP_CONFIG["email"], SMTP_CONFIG["password"])
            server.send_message(msg)
            print("📧 메일 발송 완료")
    except Exception as e:
        print("메일 발송 실패:", e)

