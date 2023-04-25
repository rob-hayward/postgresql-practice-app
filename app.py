from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, upgrade

USERNAME = 'postgresql_practice_database_user'
PASSWORD = '4ycTydQTbskjZlRTfH8MXl6kQS06FPB9'
DBNAME = 'postgresql-practice-database'
HOST = 'dpg-ch3te4aut4m1v1o5qgsg-a'

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql_practice_database_user:4ycTydQTbskjZlRTfH8MXl6kQS06FPB9@dpg-ch3te4aut4m1v1o5qgsg-a/postgresql_practice_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


if __name__ == '__main__':
    app.run(debug=True)
