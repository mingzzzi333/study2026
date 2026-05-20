from flask import Flask,render_template
from dotenv import load_dotenv
import requests
import os

load_dotenv()
client_id = os.getenv("NAVER_CLIENT_ID")
callback_url = os.getenv("NAVER_REDIRECT_URL")

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import redirect  # 추가

@app.route('/login')
def naver_login():
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={client_id}"
        f"&redirect_uri={callback_url}&state=HELLO"
    )
    return redirect(auth_url)

if __name__ == '__main__':
    app.run(debug=True)

    # response_type=code 
    # code_id=client_id  
    # redirect_url=redirect_uri  
    # state=scope