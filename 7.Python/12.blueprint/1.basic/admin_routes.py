from flask import Blueprint,render_template

admin_blueprint=Blueprint('admin',__name__)

@admin_blueprint.route('/')
def admin_page():
    return render_template('admin.html')

if __name__=='__main__':
    admin_blueprint.run(debug=True)