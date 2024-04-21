from flask import Blueprint, render_template, request, redirect, url_for
from models import Customer

# Create a Blueprint for your routes
routes = Blueprint('routes', __name__)

# Define routes
@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/cashout')
def cashout_cheque():
    return render_template('cashout_cheque.html')

@routes.route('/cheque-details')
def cheque_details():
    return render_template('cheque_details.html')

@routes.route('/signup')
def signup():
   return render_template('signup.html')
