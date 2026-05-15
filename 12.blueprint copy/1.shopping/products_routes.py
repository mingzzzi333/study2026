from flask import Blueprint,render_template

products_blueprint=Blueprint('products',__name__)

@products_blueprint.route('/')
def products_page():
    return render_template('products.html')
if __name__=='__main__':
    products_blueprint.run(debug=True)