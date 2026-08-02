# import requests

# url = "https://invalid-api.com/data"

# for i in range(5):
#     print(f"Request {i+1}")

#     try:
#         response = requests.get(url, timeout=2)
#         print(response.status_code)
#     except Exception as e:
#         print("API Failed:", e)


import requests

url = "https://invalid-api.com/data"

failure_count = 0
MAX_FAILURES = 3

for i in range(5):

    print(f"\nRequest {i+1}")

    # Circuit Breaker
    if failure_count >= MAX_FAILURES:
        print("🚫 Circuit Open - Skipping API Call")
        continue

    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        print("Success")
        failure_count = 0      # Reset on success

    except Exception:
        failure_count += 1
        print(f"API Failed ({failure_count}/{MAX_FAILURES})")