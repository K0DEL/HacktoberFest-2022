from flask import Flask, render_template, jsonify, abort, request
from handlers.Internfreak import fetch_posts
from handlers.Myanimelist import MAL
from handlers.Fakku import Fakku
import handlers.bypassers as bypassers
from blueprints.urbanDictionary import urbanDictionary
from dateutil import relativedelta
from datetime import datetime
import json
import random
import requests

from blueprints.user import user_blueprint
from blueprints.post import post_blueprint
from prisma import Prisma, register

db = Prisma()
db.connect()
register(db)
app = Flask(__name__)

# https://github.com/herbalchappal 
app.register_blueprint(urbanDictionary)
############## END ################

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(post_blueprint, url_prefix='/post')


@app.errorhandler(404)
def handle_404(e):
    return render_template("error.html"), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/internfreak/latest",methods=["GET"])
def internfreak():
    posts = fetch_posts()
    if posts:
        return jsonify(posts)
    else:
        abort(404, description="Resource not found")



@app.route('/anime/<mal_id>',methods=["GET"])
def myanimelist(mal_id):
    anime_info = MAL(mal_id)
    return jsonify(anime_info)

@app.route('/fakku/<id>',methods=["GET"])
async def fakku(id):
    url = "https://www.fakku.net/hentai/" + id
    doujin_info = await Fakku.scrape(url)
    return jsonify(doujin_info)

@app.route("/date_between", methods=["POST"])
def date_between():
    try:
        args = request.args
        args = args.to_dict()
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        if start_date is None or end_date is None:
            return {"error": "start_date or end_date cannot be empty."}

        d1 = datetime.strptime(start_date, "%d/%m/%Y")
        d2 = datetime.strptime(end_date, "%d/%m/%Y")
        deltaRelative = relativedelta.relativedelta(d2, d1)
        return {
            "delta": {
                "days": deltaRelative.days,
                "months": deltaRelative.months,
                "years": deltaRelative.years,
            },
            "start_date": start_date,
            "end_date": end_date,
        }
    except Exception as e:
        return {"error": str(e)}


@app.route("/bypass", methods=["POST"])
def bypass_links():

    data = request.data.strip()
    if len(data) == 0:
        return jsonify({"ok": False, "message": "No data provided"})

    try:
        data = json.loads(data)
    except json.JSONDecodeError as ex:
        return jsonify({"ok": False, "message": "Could not parse the data as JSON"})
    data_keys = data.keys()
    if len(data_keys) != 2 or "type" not in data_keys or "url" not in data_keys:
        return jsonify(
            {"ok": False, "message": "Exactly two keys required: 'type' and 'url'"}
        )

    bypasser_type, url_to_bypass = data["type"], data["url"]
    if bypasser_type not in bypassers.BYPASSERS.keys():
        return jsonify({"ok": False, "message": "Not a valid bypasser"})

    bypasser_func = bypassers.BYPASSERS[bypasser_type]
    try:
        bypassed_link = bypasser_func(url_to_bypass)
    except Exception as ex:
        return jsonify({"ok": False, "message": f"Failed to bypass: {ex}"})

    return jsonify({"ok": True, "url": bypassed_link})

@app.route("/meme_template",methods=["POST","GET"])
def memer():
    data=requests.get('https://api.imgflip.com/get_memes')
    data=data.json()["data"]["memes"]
    a=random.randint(1,99)
    data=data[a]["url"]
    return render_template("temp.html",data=data)

@app.route("/Animal/<an>",methods=["GET","POST"])
def ip(an):
    data=requests.get("https://dog.ceo/api/breeds/image/random")
    data1=requests.get("https://aws.random.cat/meow?ref=apilist.fun")
    data=data.json()["message"]
    data1=data1.json()["file"]
    Mess="Only Cat and Dog are available"
    if(an=="cat"):
        return render_template("animal.html",data=data1)
    elif(an=="dog"):
        return render_template("animal.html",data=data)
    else: 
        return jsonify(Mess)
    
    
    

if __name__ == "__main__":
    app.run(host="localhost", port=3000, threaded=True)
