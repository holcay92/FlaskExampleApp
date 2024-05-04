from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, app
from models import Customer, Cheque
from routes.index_routes import index_routes
from routes.cheque_routes import cheque_routes
from routes.auth_routes import auth_routes

routes = Blueprint('routes', __name__)


@routes.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        cheque_history = Cheque.query.filter_by(user_id=user_id).all()
        user = Customer.query.get(user_id)
        return render_template('dashboard.html', cheque_history=cheque_history,user=user)
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('routes.login'))
    

app.register_blueprint(routes)
app.register_blueprint(index_routes)
app.register_blueprint(cheque_routes)
app.register_blueprint(auth_routes)

if __name__ == '__main__':
    app.run(debug=True)
