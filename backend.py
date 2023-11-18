from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests
import numpy as np
import pandas as pd

app = Flask(__name__)

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
STOCK_DATA_SERVICE_URL = "http://localhost:5001"

@app.route('/predict', methods=['POST'])
def predict_stock_price():
    data = request.json
    symbol = data.get('symbol')
    period = data.get('period', '1y')

    # Call the Stock Data Service
    response = requests.post(f"{STOCK_DATA_SERVICE_URL}/fetch", json={'symbol': symbol, 'period': period})
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch stock data"}), 500

    # Convert response to DataFrame
    stock_data = pd.DataFrame(response.json())
    stock_data.reset_index(inplace=True)
    
    # Prepare data for prediction
    X = np.array(stock_data.index).reshape(-1, 1)
    y = stock_data['Close']

    # Train-test split
    X_train, X_test, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Linear Regression Model
    model = LinearRegression().fit(X_train, y_train)
    predicted_price = model.predict([[len(stock_data)]])[0]

    # Save prediction to database
    new_prediction = Prediction(symbol=symbol, predicted_price=predicted_price)
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({"prediction": predicted_price})

@app.route('/')
def index():
    return render_template('frontend.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will now execute within the app's context
    app.run(port=5000)

