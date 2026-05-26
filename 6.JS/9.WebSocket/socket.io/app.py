from flask import Flask, send_from_directory
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "my-secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")  # ← 이거 추가

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@socketio.on('message')
def handle_message(msg):
    print("Message:", msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)