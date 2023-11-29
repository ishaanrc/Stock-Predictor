from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch_stock_data():
    print("IN FETCH")
    data = request.json
    symbol = data.get('symbol')
    period = data.get('period', '10y')

    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        print(len(history))
        
        # Convert Timestamps to strings
        history.index = history.index.strftime('%Y-%m-%d')

        return jsonify(history.to_dict())
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
