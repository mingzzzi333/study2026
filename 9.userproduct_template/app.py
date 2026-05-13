from flask import Flask,jsonify,request,render_template

# 1. /user 라는 경로를 만들고 URL파라미터를 기반으로 사용자를 조회할수 있게 한다.
#    /user는 모든 사용자 /user/1 홍길동 /user/2 김철수 등
# 2. /product 로 쿼리 파라미터를 기반으로 상품을 조회할수 있다
#    /product는 모든 상품, /product?id=101 로 상품 검색 ?name 으로도 상품 검색

app = Flask(__name__)

#id,name,email
users = {
    1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
    3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
    4: {"id": 4, "name": "박민수", "email": "park@example.com"},
    5: {"id": 5, "name": "최지우", "email": "choi@example.com"},
}

#id,name,price
products = {
    101: {"id": 101, "name": "Laptop", "price": 1200},
    102: {"id": 102, "name": "Keyboard", "price": 80},
    103: {"id": 103, "name": "Mouse", "price": 40},
    104: {"id": 104, "name": "Monitor", "price": 300},
    105: {"id": 105, "name": "Headset", "price": 150},
}

@app.route("/")
def home():
    return render_template("index.html", products=list(products.values()))

@app.route('/user')
def get_users():
    return jsonify(list(users.values()))

@app.route('/user/<int:id>')
def get_user(id):
    user = users.get(id)
    if user:
        return jsonify(user)
    return jsonify({"message": "사용자를 찾을 수 없습니다."})

@app.route('/product/view')
def product_view():
    return render_template('product.html', products=list(products.values()))

@app.route('/product')
def get_products():
    id= request.args.get('id', type=int)
    name = request.args.get('name')

    if id:
        product = products.get(id)
        if product:
            return jsonify(product)
        return jsonify({"message": "상품 찾을 수 없습니다."})
        
    if name:
        result = [p for p in products.values() if name.lower() in p['name'].lower()]
        return jsonify(result)
    
    return jsonify(list(products.values()))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
