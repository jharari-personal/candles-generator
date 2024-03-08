import logging
import os
from flask import Flask, request, jsonify
from candles import generate_candles 

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='flask_errors.log', level=logging.ERROR)


@app.route('/get_candles', methods=['GET'])
def endpoint():
    try:
        # Assuming your script takes two parameters from the request
        rate = float(request.args.get('rate'))
        timeframe = str(request.args.get('timeframe'))
        numCandles = int(request.args.get('numCandles'))

        # Call your existing script function with the parameters
        result = generate_candles(rate, timeframe, numCandles)

        # Create a response JSON
        response = {'result': result}

        return jsonify(response)

    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
