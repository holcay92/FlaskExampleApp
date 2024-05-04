from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from datetime import datetime, timezone
from models import Customer

auth_routes = Blueprint('auth_routes', __name__)




@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']
        user = Customer.query.filter_by(email=email).first()
        if user.check_password(password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
        return redirect(url_for('routes.login'))

@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['name']
        last_name = request.form['surname']
        phone_number = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        if not all([first_name, last_name, phone_number, email, password]):
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('routes.signup'))
        
        created_at = datetime.now(timezone.utc)
        country = 'Türkiye'
        is_verified = False

        new_customer = Customer(
            first_name=first_name, 
            last_name=last_name, 
            phone_number=phone_number, 
            email=email, 
            password=password, 
            created_at=created_at, 
            country=country, 
            is_verified=is_verified
        )

        db.session.add(new_customer)
        db.session.commit()

        flash('Sign up successful! You can now log in.', 'success')
        return redirect(url_for('index_routes.index'))
    else:
        return render_template('signup.html')

@auth_routes.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index_routes.index')) 
