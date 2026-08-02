# This code demonstrates how to handle timeouts when making API calls using the requests library in Python. The code attempts to call an API endpoint that has a delay of 10 seconds, but it sets a timeout of 3 seconds for the request. If the request takes longer than 3 seconds, a Timeout exception is raised, and the program prints "Request Timed Out!" instead of waiting indefinitely for a response. The total time taken for the request is also printed at the end.

# import requests
# import time

# url = "https://httpbin.org/delay/10"

# start = time.time()

# print("Calling API...")

# response = requests.get(url)      # No timeout

# print(response.status_code)

# print("Time Taken:", round(time.time() - start, 2), "seconds")

import requests
import time

url = "https://httpbin.org/delay/10"

start = time.time()

try:
    print("Calling API...")

    response = requests.get(url, timeout=3)

    print(response.status_code)

except requests.exceptions.Timeout:
    print("Request Timed Out!")

print("Time Taken:", round(time.time() - start, 2), "seconds")