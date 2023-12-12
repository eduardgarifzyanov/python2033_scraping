from flask import Flask
import flask_sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = flask_sqlalchemy.SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    author = db.Column(db.String(300))
    price = db.Column(db.String(300))
    publishing = db.Column(db.String(300))
    year_release = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    description = db.Column(db.Text)
    url = db.Column(db.String(300))
    