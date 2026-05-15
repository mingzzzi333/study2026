from flask import Flask,render_template

from admin_routes import admin_blueprint
from user_routes import user_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint,url_prefix="/user")
app.register_blueprint(admin_blueprint,url_prefix="/admin")


@app.route('/')
def home():
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)