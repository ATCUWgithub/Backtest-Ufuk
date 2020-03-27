from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve

from error import InvalidUsage
from stockFilter import prep_all
from stockFilter import get_all_data
from stockFilter import get_chart_data
from stockFilter import get_pricing
from stockFilter import getOpens

app = Flask(__name__)
CORS(app)


def has_args(iterable, args):
    """Verify that all args are in the iterable."""

    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
def ping():
    return 'API is Running'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/getData', methods=['POST'])
def updateOpenPrices():
    print(request)
    print(request.json)
    if not has_args(request.json, ['ticker']):
        raise InvalidUsage('Please provide ticker to get the open price for.')

    # response = jsonify(error.to_dict())
    # response.status_code = error.status_code

    # updates the opening prices dictionary in stockFilter
    data = get_all_data(request.json['ticker'])
    data_json = jsonify(data)
    return data_json

@app.route('/getCharting', methods = ['POST'])
def charting():
    if not has_args(request.json, ['ticker']):
        raise InvalidUsage('Please provide ticker to get the chart data for.')
    data = get_chart_data(request.json['ticker'])
    data_json = data
    return data_json


@app.route('/getPricingUpdate', methods=['POST'])
def pricing():
    if not has_args(request.json, ['ticker']):
        raise InvalidUsage('Please provide ticker to get the chart data for.')
    data = get_pricing(request.json['ticker'])
    data_json = jsonify(data)
    return data_json

@app.route('/getAll', methods = ['GET'])
def getAll():
    data = prep_all()
    data_json = jsonify(data)
    return data_json

@app.route('/getOpens', methods=['GET'])
def gettingOpens():
    getOpens()
    return 'done!'


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)


serve(app, host='0.0.0.0', port=5000, threads=350)
