from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the database URI            database://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

# Define a Flask CLI command to create database tables
@app.cli.command()
def create_tables():
    with app.app_context():
        db.create_all()
        print('Database tables created')

@app.route('/')
def index():
    person =Person.query.first()
    return 'Hello ' + person.name

if __name__ == '__main__':
  
    app.run(debug=True)
