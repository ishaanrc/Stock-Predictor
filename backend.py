from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests
import numpy as np
import pandas as pd
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1"}})

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)

# URL of the Stock Data Service
STOCK_DATA_SERVICE_URL = "http://127.0.0.1:5001"

@app.route('/predict', methods=['POST'])
def predict_stock_price():
    print("HEEEEEEE")
    data = request.json
    symbol = data.get('symbol')
    period = data.get('period', '1y')
    print("DATA", data)
    print("RESPONSE:")
    # Call the Stock Data Service
    response = requests.post(f"{STOCK_DATA_SERVICE_URL}/fetch", json={'symbol': symbol, 'period': period})
    print("Response:",response)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch stock data"}), response.status_code
    print("PAST RESPONSE")
    # Convert response to DataFrame
    stock_data = pd.DataFrame(response.json())
    
    # Perform prediction
    predicted_price = perform_prediction(stock_data)

    # Save prediction to database
    new_prediction = Prediction(symbol=symbol, predicted_price=predicted_price)
    db.session.add(new_prediction)
    db.session.commit()

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
    return render_template('frontend.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will now execute within the app's context
    app.run(port=5000, debug=True)
