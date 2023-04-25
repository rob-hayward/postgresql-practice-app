from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, upgrade
import os

app = Flask(__name__)

LOCAL_USERNAME = 'rob_hayward'
LOCAL_PASSWORD = 'new_password'
LOCAL_DBNAME = 'testdb'
DATABASE_URL = os.environ.get('DATABASE_URL') \
               or f'postgresql://{LOCAL_USERNAME}:{LOCAL_PASSWORD}@localhost/{LOCAL_DBNAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('index.html', users=users)


print("Using database:", DATABASE_URL)

if __name__ == '__main__':
    app.run(debug=True)
