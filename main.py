from flask import Flask, render_template, jsonify, abort
from handlers.Internfreak import fetch_posts

app = Flask(__name__)


@app.errorhandler(404)
def handle_404(e):
    return render_template('error.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/internfreak/latest')
def internfreak():
    posts = fetch_posts()
    if posts:
        return jsonify(posts)
    else:
        abort(404, description="Resource not found")


if __name__ == '__main__':
    app.run(host="localhost", port=3000, threaded=True)
