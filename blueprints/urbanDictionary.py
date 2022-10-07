# github.com/herbalchappal
from flask import Blueprint, render_template, request, jsonify
import requests

urbanDictionary = Blueprint('urbanDictionary', __name__, template_folder='templates')


@urbanDictionary.route("/urbanDictionary", methods=["GET"])
def renderTemplate():
    return render_template("urbanDictionary.html", len=0, results=[])


@urbanDictionary.route("/urbanDictionary", methods=['POST'])
def getResultsFromUrbanDictionary():
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    query = request.form.get("query")

    querystring = {"term": query}

    headers = {
        "X-RapidAPI-Key": "<-your-rapid-api-key->",
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    return render_template("urbanDictionary.html", query=query, len=len(response['list']), results=response)
# END
