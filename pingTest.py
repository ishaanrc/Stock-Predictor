import requests
import json
import time

# Replace with the actual IP and port of your Flask app
FLASK_APP_URL = "https://cloudrunservice-76w3cwh3pa-wl.a.run.app/predict"
avg=[]
def test_predict_endpoint(symbol, period):
    data = {'symbol': symbol, 'period': period}

    # Measure the time before making the request
    start_time = time.time()
    print(start_time)

    # Make the request to the Flask app
    response = requests.post(FLASK_APP_URL, json=data)

    # Measure the time after receiving the response
    end_time = time.time()
    print(end_time)
    elapsed_time = end_time - start_time
    print(elapsed_time*1000)

    if response.status_code == 200:
        result = response.json()
        prediction = result.get('prediction')
        response_time = result.get('response_time')
        print(f"Prediction: {prediction}")
        avg.append(elapsed_time*1000)
        print(f"Response Time: {elapsed_time*1000} seconds")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Replace 'AAPL' with the actual stock symbol and adjust the period as needed
    for i in range(0,50):
        test_predict_endpoint(symbol='AAPL', period='1y')

    average_response_time = sum(avg) / len(avg)
    print(f"Average Response Time: {average_response_time} milliseconds")

