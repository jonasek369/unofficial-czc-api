import json
import os

import redis
from flask import Flask, render_template, request

from Logger import *
from czcParser import Parser
from errors import *

parser = Parser()

app = Flask(__name__)

DEFAULT_REDIS_EXPIRE = 600
rds = redis.Redis()

os.system("cls")

try:
    rds.keys()
    LOG(SUCCESS, "Connected to redis database")
except redis.exceptions.ConnectionError or any:
    LOG(ERROR, "Connection to redis database failed")
    exit(1)


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/api/product-info')
def product_info():
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        redis_fetch = rds.get(f"product-info:{identifier}")
        if redis_fetch is None:
            if identifier is None:
                return throw_missing_parameters(["identifier"])
            data = parser.get_product_info(f"https://www.czc.cz/a/{identifier}/produkt")
            rds.setex(f"product-info:{identifier}", DEFAULT_REDIS_EXPIRE, json.dumps(data))
            return data
        else:
            return json.loads(redis_fetch)
    except KeyError:
        return throw_json_error()


@app.route('/api/list-info')
def list_info():
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        redis_fetch = rds.get(f"list-info:{identifier}")
        if redis_fetch is None:
            if identifier is None:
                return throw_missing_parameters(["identifier"])
            data = parser.get_seznam_info(f"https://www.czc.cz/{identifier}/seznam")
            rds.setex(f"list-info:{identifier}", DEFAULT_REDIS_EXPIRE, json.dumps(data))
            return data
        else:
            return json.loads(redis_fetch)
    except KeyError:
        return throw_json_error()
