import requests
import time

url = "https://cloudrunservice-76w3cwh3pa-wl.a.run.app"
num_requests = 50
total_time = 0

for _ in range(num_requests):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    if response.status_code == 200:
        elapsed_time = end_time - start_time
        total_time += elapsed_time
    else:
        print(f"Request failed with status code {response.status_code}")

average_time = total_time / num_requests
print(f"Average time to load the page: {average_time} seconds")
