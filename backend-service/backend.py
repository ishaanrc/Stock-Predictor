from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
#CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1"}})

# URL of the Stock Data Service
STOCK_DATA_SERVICE_URL = "http://54.183.201.14:5001"

@app.route('/predict', methods=['POST'])
def predict_stock_price():
    data = request.json
    symbol = data.get('symbol')
    period = data.get('period', '10y')

    # Call the Stock Data Service
    response = requests.post(f"{STOCK_DATA_SERVICE_URL}/fetch", json={'symbol': symbol, 'period': period})
    print(response)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch stock data"}), response.status_code

    # Convert response to DataFrame
    stock_data = pd.DataFrame(response.json())
    print(len(stock_data))
    
    # Perform prediction
    predicted_price = perform_prediction(stock_data)

    return jsonify({"prediction": predicted_price})

def perform_prediction(stock_data):
    stock_data.reset_index(inplace=True)
    X = np.array(stock_data.index).reshape(-1, 1)
    y = stock_data['Close']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression().fit(X_train, y_train)
    return model.predict([[len(stock_data)]])[0]

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stock Predictor</title>
        <script>
            async function predict() {
                let symbol = document.getElementById("symbol").value;
                let period = document.getElementById("period").value;

                try {
                    let response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({symbol: symbol, period: period})
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response}`);
                    }

                    let data = await response.json();
                    document.getElementById("result").innerText = JSON.stringify(data);
                } catch (error) {
                    console.error("Error caught:", error);
                    document.getElementById("result").innerText = 'Error: ' + error.message;
                }
            }
        </script>
    </head>
    <body>
        <h1>Stock Predictor</h1>
        <input type="text" id="symbol" placeholder="Enter Stock Symbol">
        <select id="period">
            <option value="1d">1d</option>
            <option value="5d">5d</option>
            <option value="1mo">1mo</option>
            <option value="3mo">3mo</option>
            <option value="6mo">6mo</option>
            <option value="1y" selected>1y</option>
            <option value="10y" selected>10y</option>
        </select>
        <button onclick="predict()">Predict</button>

        <h2>Result:</h2>
        <div id="result"></div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
