from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import os
import app

load_dotenv()

NAVER_ID = os.getenv('NAVER_MAIL_ID')
NAVER_PASSWORD = os.getenv('NAVER_MAIL_APP_SECRET')
NAVER_EMAIL = f"{NAVER_ID}@naver.com"

SMTP_SERVER = "smtp.naver.com"
SMTP_PORT = 587

subject = "네이버 메일 보내기 테스트중"
body = "이메일은 파이썬을 통해서 작성되었습니다."

message = MIMEText(body, _charset='utf-8')
message['Subject'] = subject
message['From'] = NAVER_EMAIL
message['To'] = NAVER_EMAIL

try:
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(NAVER_ID, NAVER_PASSWORD)
    smtp.sendmail(NAVER_EMAIL, NAVER_EMAIL, message.as_string())
    smtp.quit()
    print("메일 전송 성공!")
except Exception as e:
    print(f"메일 전송 실패: {e}")