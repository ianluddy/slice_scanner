from flask import request
from slice_scanner.utils import json_response
from slice_scanner import app
from slice_scanner import db_wrapper as db

@app.route('/')
def index():
    return app.send_static_file('index.html')

### Pizza API ####

@app.route('/pizza')
def pizza():
    data, count = db.get_pizza(
        toppings=request.args.get("toppings"),
        style=request.args.get("style"),
        base_style=request.args.get("base_style"),
        diameter=request.args.get("diameter", []),
        vendor=request.args.get("vendor"),
        slices=request.args.get("slices", []),
        price=request.args.get("price", []),
        score=request.args.get("score", []),
        sort_by=request.args.get("sort_by"),
        sort_dir=request.args.get("sort_dir"),
        page=request.args.get("page"),
    )
    return json_response(data, count=count)

@app.route('/pizza/toppings')
def pizza_toppings():
    return json_response(db.distinct("pizza", "toppings"), sort=True)

@app.route('/pizza/diameters')
def pizza_diameters():
    return json_response(db.range("pizza", "diameter"))

@app.route('/pizza/styles')
def pizza_styles():
    return json_response(db.distinct("pizza", "style"), sort=True)

@app.route('/pizza/slices')
def pizza_slices():
    return json_response(db.range("pizza", "slices"))

@app.route('/pizza/bases')
def pizza_bases():
    return json_response(db.distinct("pizza", "base_style"), sort=True)

@app.route('/pizza/sizes')
def pizza_sizes():
    return json_response(db.range("pizza", "size"))

@app.route('/pizza/prices')
def pizza_prices():
    return json_response(db.range("pizza", "price"))

@app.route('/pizza/scores')
def pizza_scores():
    return json_response(db.range("pizza", "score"))

### Side API ####

@app.route('/sides')
def sides():
    data, count = db.get_sides(
        type=request.args.get("type"),
        vendor=request.args.get("vendor", []),
        price=request.args.get("price", []),
        sort_by=request.args.get("sort_by"),
        sort_dir=request.args.get("sort_dir"),
        page=request.args.get("page")
    )
    return json_response(data, count=count)

@app.route('/sides/types')
def sides_types():
    return json_response(db.distinct("sides", "type"), sort=True)

@app.route('/sides/prices')
def sides_prices():
    return json_response(db.range("sides", "price"))

### Vendor API ####

@app.route('/vendors')
def vendors():
    return json_response(db.distinct("pizza", "vendor"), sort=True)

### Stats API ####

@app.route('/stats')
def stats():
    return json_response({
        "pizza": db.count("pizza"),
        "sides": db.count("sides"),
        "desserts": db.count("desserts"),
        "drinks": db.count("drinks"),
        "combos": db.count("combos"),
        "vendors": len(db.distinct("pizza", "vendor"))
    })