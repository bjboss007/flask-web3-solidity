from flask import app, json, Blueprint, request
from web3 import method
from .deploy import retrieveFunction, storeFunction


app = Blueprint('posts',__name__)

@app.route("/home")
def home():
    return json.jsonify({"name":"Mobolaji","age":24}), 200

@app.route("/retrieve")
def retrieve():
    try :
        return json.jsonify({"value":retrieveFunction()}), 200
    except ValueError as err:
        return json.jsonify({"error": str(err)}), 403

@app.route("/store", methods = ["POST"])
def store():
    dict_value = request.get_json(force=True)
    number = dict_value["number"]

    try:
        result = storeFunction(number)
    except ValueError as err:
        return json.jsonify({"error":str(err)}), 403


    return json.jsonify({"message": result}), 200
