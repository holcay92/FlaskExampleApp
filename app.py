from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#                                        dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        # Inside the app context, create the database tables
        db.create_all()
@app.route('/')

def index():
  return 'Hello World!'