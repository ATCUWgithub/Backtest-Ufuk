from flask import Flask, jsonify, request
from waitress import serve

from error import InvalidUsage

from stockFilter import get_stock_pool
from stockFilter import getOpenPrices
from stockFilter import get_drawdowns

app = Flask(__name__)


def has_args(iterable, args):
    """Verify that all args are in the iterable."""

    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
def ping():
    return 'API running.'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/updateStockPool', methods=['POST'])
def update_stock_pool():
    # updates the stock pool in stockFilter
    get_stock_pool()
    return 'Stock pool has been updated'


@app.route('/updateOpenPrices', methods=['POST'])
def updateOpenPrices():
    # updates the opening prices dictionary in stockFilter
    prices = getOpenPrices()
    return prices


@app.route('/getDrawdowns', methods=['POST'])
def getDrawdowns():
    # returns a json of {tickerSymbol:percentDrawDown} for all tickerSymbols with
    # drawdowns between 1%-2% since the market open
    return get_drawdowns()


if __name__ == '__main__':
    app.debug = True
    app.run()


serve(app, host='0.0.0.0', port=3000)
