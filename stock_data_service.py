from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch_stock_data():
    data = request.json
    symbol = data.get('symbol')
    period = data.get('period', '1y')

    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        return jsonify(history.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
