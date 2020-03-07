from flask import Flask, jsonify, request
from waitress import serve

from error import InvalidUsage

from stockFilter import EquityScreener
from stockFilter import serveOpenPrices
from stockFilter import serveCurPrices
from stockFilter import dd


app = Flask(__name__)
es = EquityScreener()

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

@app.route('/serveData', methods=['GET'])
def serveData():
    print(es.serveData())
    return jsonify({'I give you': es.serveData()})

@app.route('/updateStockPool', methods=['POST'])
def update_stock_pool():
    # updates the stock pool in stockFilter
    es.get_stock_pool()
    return 'Stock pool has been updated'

@app.route('/getPrice', methods=['POST'])
def getPrice():
    # updates the stock pool in stockFilter
    es.getCurPrice(request.json['Stock'])
    return jsonify({'I give you': es.serveData()})

#@app.route('/DONOTUSE', methods=['POST'])
#def DONOTUSE():
    # updates the stock pool in stockFilter
#    es.testUpdate(request.json['Key'])
#    return jsonify({'I give you' : es.serveData()})


@app.route('/updateOpenPrices', methods=['GET'])
def updateOpenPrices():

    #response = jsonify(error.to_dict())
    #response.status_code = error.status_code

    # updates the opening prices dictionary in stockFilter
    es.getOpenPrices()
    return jsonify(serveOpenPrices())

#MUST BE HAPPENING ASYNC
@app.route('/updateCurPrices', methods=['GET'])
def updateCurPrices():

    #response = jsonify(error.to_dict())
    #response.status_code = error.status_code

    # updates the opening prices dictionary in stockFilter
    es.updateCurPrices()
    return jsonify(serveCurPrices())


#@app.route('/updateOpenPrice', methods=['POST'])
#def updateOpenPrice():
#    if not has_args(request.json, ['ticker']):
#        raise InvalidUsage('Please provide ticker to get the open price for.')#
#
#    open_price = getOpenPrice(request.json['ticker'])
#    return jsonify({'ticker': request.json['ticker'], 'Open Price': open_price})


@app.route('/getDrawdowns', methods=['GET'])
def getDrawdowns():
    # returns a json of {tickerSymbol:percentDrawDown} for all tickerSymbols with
    # drawdowns between 1%-2% since the market open
    
    #ASSUMING UPDATECURPRICES IS HAPPENING ASYNC, CURPRICES.JSON IS RELEVANT

    return jsonify(dd())

if __name__ == '__main__':
    app.debug = True
    app.run()


serve(app, host='0.0.0.0', port=3000)
