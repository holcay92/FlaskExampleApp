from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models.Customer import Customer

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/cashout')
def cashout_cheque():
    return render_template('cashout_cheque.html')

@routes.route('/cheque-details')
def cheque_details():
    return render_template('cheque_details.html')

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("POST method is being executed correctly.")
        # Get form data
        first_name = request.form['name']
        last_name = request.form['surname']
        phone_number = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        created_at = datetime.now(timezone.utc)
        country = 'Türkiye'
        is_verified = False
        # Create a new customer
     
        new_customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password, created_at=created_at, country=country, is_verified=is_verified)
        print(new_customer)
        db.session.add(new_customer)
        # Commit the transaction
        db.session.commit()
        flash('Sign up successful! You can now log in.', 'success')
        return redirect(url_for('routes.index'))
    else:
        return render_template('signup.html')
    


