from flask import Flask, jsonify, request
from waitress import serve

from error import InvalidUsage
from reccomend import matching_score

app = Flask(__name__)


def has_args(iterable, args):
    """Verify that all args are in the iterable."""

    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
def ping():
    return 'Jarvis, start the engines.'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/getReccomendations', methods=['POST'])
def reccomend_book():

    if not has_args(request.json, ['numResponses']):
        raise InvalidUsage(
            'Please provide the number of responses you want to recieve.')

    if not has_args(request.json, ['query']):
        raise InvalidUsage('Please provide a query to match with.')

    query, titles = matching_score(
        request.json['numResponses'], request.json['query'])

    return jsonify({'query': query, 'query': titles})


# if __name__ == '__main__':
#     app.run()


serve(app, host='0.0.0.0', port=3000)
