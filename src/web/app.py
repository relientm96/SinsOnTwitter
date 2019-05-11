# -*- encoding: utf-8 -*-
#
# flask app

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    """
    home page
    :return: html template
    """
    option_list = [
        {"sin": "Lust", "states": ["New South Wales"], "databases": ["Rape", "Sexual Offences"]},
        {"sin": "Wraith", "states": ["All", "New South Wales", "South Australia"], "databases": ["Violence", "Street Brawl"]},
        {"sin": "Sloth", "states": ["Victoria", "Queensland"], "databases": ["Strike"]},
        {"sin": "Greed", "states": ["Tasmania"], "databases": ["Robbery", "Theft"]},
    ]
    return render_template("home.html", option_list=option_list)


@app.route('/sin', methods=['GET'])
def get_options():
    """
    get state and aurin database name option by choosing sin
    :return:
    """
    result = dict()
    try:
        sin = request.json["sin"]
    except Exception as e:
        print(e)
    return jsonify(result)


@app.route('/search', methods=['POST'])
def search():
    try:
        keyword_list = request.json["keywords"]
        sin = request.json["sin"]
        state = request.json["state"]
        database_list = request.json["databases"]
        chart = request.json["chart"]
        print(str(keyword_list))
        print(str(database_list))
        print(sin + " " + chart + " " + state)
    except Exception as e:
        print(e)
    return jsonify()


@app.route('/bar_chart')
def bar():
    return render_template("home.html", content="this is a testing")


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

if __name__ == '__main__':
    app.run()