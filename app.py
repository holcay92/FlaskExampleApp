from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#                                        dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)



@app.route('/')
def index():
    return 'Hello, World!'