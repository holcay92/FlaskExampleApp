from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, app
from datetime import datetime, timezone
from models import Customer, Cheque

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/cashout', methods=['GET', 'POST'])
def cashout_cheque():
    if request.method == 'POST':
        email = request.form['email']
        cheque_id = request.form['chequeId']
        user = Customer.query.filter_by(email=email).first()
        cheque = Cheque.query.filter_by(cheque_id=cheque_id, user_id= user.id).first()
        cheque_sender_user = Customer.query.filter_by(id=cheque.receiver_customer_id).first()
        if user.balance is None:
            user.balance = 0.0
        if cheque and cheque.status != 'Cashed Out':
            balance = user.balance
            cheque_sender_user.balance -= cheque.amount
            user.balance += cheque.amount    
            cheque.status = 'Cashed Out'
            db.session.commit()
            flash('Cheque cashed out successfully!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or cheque ID. Please try again.', 'danger')

    return render_template('cashout_cheque.html')

@routes.route('/deposit', methods=['GET', 'POST'])
def deposit_cheque():
    if request.method == 'POST':
        email = request.form['email']
        receiver_email = request.form['receiver-email']
        cheque_id = request.form['chequeId']
        amount = request.form['amount']
        bank = request.form['bank']
        cashing_date = request.form['date']

        if not email or not receiver_email or not cheque_id or not amount or not bank or not cashing_date:
            flash('Please fill in all the fields.', 'danger')
            return redirect(url_for('routes.deposit_cheque'))

        user = Customer.query.filter_by(email=email).first()
        receiver_customer = Customer.query.filter_by(email=receiver_email).first()
        is_cheque_id_exist = Cheque.query.filter_by(cheque_id=cheque_id).first()

        if not user or not receiver_customer or (is_cheque_id_exist is not None and is_cheque_id_exist.status != 'Pending'):
            flash('Invalid email address or invalid check ID. Please provide valid email addresses.', 'danger')
            return redirect(url_for('routes.deposit_cheque'))
        
        new_cheque = Cheque(
            cheque_id=cheque_id,
            amount=amount,
            cash_out_date=cashing_date,
            bank=bank,
            user_id=receiver_customer.id,
            status='Pending',
            receiver_customer_id=user.id,
            created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        )

        db.session.add(new_cheque)

        try:
            db.session.commit()
            flash('Cheque details submitted successfully!', 'success')
            return redirect(url_for('routes.deposit_cheque'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('routes.deposit_cheque'))

    return render_template('deposit_cheque.html')

@routes.route('/login', methods=['GET', 'POST'])
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

@routes.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for('routes.index'))
    else:
        return render_template('signup.html')

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
    
@routes.route('/cheque/<int:cheque_id>')
def cheque_detail(cheque_id):
    cheque = Cheque.query.get(cheque_id)
    # find the user
    user = Customer.query.get(cheque.user_id)
    receiver_user = Customer.query.get(cheque.receiver_customer_id)

    if not cheque:
        flash('Cheque not found.', 'danger')
        return redirect(url_for('routes.dashboard')) 
    return render_template('cheque_detail.html', cheque=cheque, user=user,receiver_user=receiver_user)

@routes.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('routes.index')) 

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
