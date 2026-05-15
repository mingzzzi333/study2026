from flask import Flask, make_response, request
app=Flask(__name__)



@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie has been set!")
    resp.set_cookie("my_edu","study2026")
    return resp

@app.route('/get_cookie')
def get_cookie():
    cookie=request.cookies
    print(cookie)
    return f"안녕 나{cookie}야"

if __name__=='__main__':
    app.run(debug=True)