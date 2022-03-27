from flask import Flask, render_template, request

from czcParser import Parser
from errors import *

parser = Parser()

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/api/product-info')
def product_info():
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        if identifier is None:
            return throw_missing_parameters(["identifier"])
        return parser.get_product_info(f"https://www.czc.cz/a/{identifier}/produkt")
    except KeyError:
        return throw_json_error()


@app.route('/api/list-info')
def list_info():
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        if identifier is None:
            return throw_missing_parameters(["identifier"])
        return parser.get_seznam_info(f"https://www.czc.cz/{identifier}/seznam")
    except KeyError:
        return throw_json_error()
