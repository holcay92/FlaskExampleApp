from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, app
from datetime import datetime, timezone
from models import Customer, Cheque


routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/cashout')
def cashout_cheque():
    return render_template('cashout_cheque.html')

@routes.route('/cheque-details', methods=['GET', 'POST'])
def cheque_details():
    if request.method == 'POST':

        email = request.form['email']
        receiver_email = request.form['receiver-email']
        cheque_id = request.form['chequeId']
        amount = request.form['amount']
        bank = request.form['bank']
        cashing_date = request.form['date']

        user = Customer.query.filter_by(email=email).first()
        receiver_customer = Customer.query.filter_by(email=receiver_email).first()

        if not user or not receiver_customer:
            flash('Invalid email address. Please provide valid email addresses.', 'danger')
            return redirect(url_for('routes.cheque_details'))
        
        new_cheque = Cheque(
            amount=amount,
            cash_out_date=cashing_date,
            bank=bank,
            user_id=user.id,
            status='Pending',
            receiver_customer_id=receiver_customer.id,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(new_cheque)

        try:
            db.session.commit()
            flash('Cheque details submitted successfully!', 'success')
            return redirect(url_for('routes.cheque_details'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('routes.cheque_details'))

    return render_template('cheque_details.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    print("Login method is being executed correctly.")
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

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("POST method is being executed correctly.")
  
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
        db.session.commit()
        flash('Sign up successful! You can now log in.', 'success')
        return redirect(url_for('routes.index'))
    else:
        return render_template('signup.html')
    
@routes.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Fetch the user's cheque history from the database
        user_id = session['user_id']
        cheque_history = Cheque.query.filter_by(user_id=user_id).all()
        
        # Render the dashboard template with the cheque history
        return render_template('dashboard.html', cheque_history=cheque_history)
    else:
        # If the user is not logged in, redirect to the login page
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('routes.login'))

@routes.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('routes.index'))  
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
