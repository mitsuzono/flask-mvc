from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from data.database import db
from data.database import init_db
from models.user import User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db')
init_db(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/users', methods=['GET'])
def users_index():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('users/index.html', users=users)

@app.route('/users/details/<int:id>', methods=['GET'])
def users_details(id=0):
    user = User.query.get(id)
    return render_template('users/details.html', user=user)

@app.route('/users/create', methods=['GET'])
def users_create():
    return render_template('users/create.html')

@app.route('/users/create', methods=['POST'])
def users_create_post():
    user = User(username = request.form['username'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users_index'))

@app.route('/users/edit/<int:id>', methods=['GET'])
def users_edit(id=0):
    user = User.query.get(id)
    return render_template('users/edit.html', user=user)

@app.route('/users/edit', methods=['POST'])
def users_edit_post():
    id = request.form['id']
    user = User.query.get(id)
    user.username = request.form['username']
    db.session.commit()
    return redirect(url_for('users_index'))

@app.route('/users/delete', methods=['POST'])
def users_delete_post():
    id = request.form['id']
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_index'))
