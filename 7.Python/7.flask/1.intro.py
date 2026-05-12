# pip install flask
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <head>
        <title>ㅎㅇ</title>
        <style>
            p {
                color: Green
            }
        </style>
    </head>
    <body>
        <h1>ㅎㅇㅎㅇ</h1>
        <p>본문</p>
        <p>잉?</p>
    </body>
"""

if __name__ == '__main__':
    app.run()