from flask import Flask, render_template, jsonify, abort, request
from handlers.Internfreak import fetch_posts
from dateutil import relativedelta
from datetime import datetime

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

@app.route('/date_between')
def date_between():
    try:
        args = request.args
        args = args.to_dict()
        start_date = args.get('start_date')
        end_date = args.get('end_date')

        if(start_date is None or end_date is None):
            return {
                "error": "start_date or end_date cannot be empty."
            }

        d1 = datetime.strptime(start_date, "%d/%m/%Y")
        d2 = datetime.strptime(end_date, "%d/%m/%Y")
        deltaRelative = relativedelta.relativedelta(d2, d1)
        return {
            "delta": {
                "days": deltaRelative.days,
                "months": deltaRelative.months,
                "years": deltaRelative.years
            },
            "start_date": start_date,
            "end_date": end_date
        }
    except Exception as e:
        return {
            "error": str(e)
        }

if __name__ == '__main__':
    app.run(host="localhost", port=3000, threaded=True)

