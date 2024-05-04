from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from datetime import datetime, timezone
from models import Customer, Cheque

cheque_routes = Blueprint('cheque_routes', __name__)



@cheque_routes.route('/deposit', methods=['GET', 'POST'])
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

@cheque_routes.route('/cashout', methods=['GET', 'POST'])
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

@cheque_routes.route('/cheque/<int:cheque_id>')
def cheque_detail(cheque_id):
    cheque = Cheque.query.get(cheque_id)
    # find the user
    user = Customer.query.get(cheque.user_id)
    receiver_user = Customer.query.get(cheque.receiver_customer_id)

    if not cheque:
        flash('Cheque not found.', 'danger')
        return redirect(url_for('routes.dashboard')) 
    return render_template('cheque_detail.html', cheque=cheque, user=user,receiver_user=receiver_user)