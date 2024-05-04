from flask import Blueprint, render_template

index_routes = Blueprint('index_routes', __name__)

@index_routes.route('/')
def index():
    return render_template('index.html')
