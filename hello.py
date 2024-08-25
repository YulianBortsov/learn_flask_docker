from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import os

app = Flask(__name__)

# Database configuration
db_user = os.getenv('DB_USER', 'flask')
db_password = os.getenv('DB_PASSWORD', 'flask123')
db_host = os.getenv('DB_HOST', 'db')
db_name = os.getenv('DB_NAME', 'flaskDB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
@app.route('/user/<username>')
def show_user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return f'User {escape(user.username)}, Email: {escape(user.email)}'

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')

    username = request.form.get('username')
    email = request.form.get('email')
    if username in email:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        message = 'User added successfully!'
        return render_template('add_user.html', message=message, message_class='success')
    message = 'Failed to add user. Please provide both username and email. The email should contain the username.'
    return render_template('add_user.html', message=message, message_class='error')


@app.route("/hello")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_users')
def list_users():
    users = User.query.all()
    user_list = '<ul>'
    for user in users:
        user_list += f'<li>{escape(user.username)} - {escape(user.email)}</li>'
    user_list += '</ul>'
    
    return render_template('list_users.html', user_list=user_list)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

@app.route("/admin")
def admin():
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
