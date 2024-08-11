from flask import Flask, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/hello")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'

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
