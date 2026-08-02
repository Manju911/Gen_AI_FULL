# This code demonstrates a simple weather fetching function with reliability patterns such as retries, timeouts, and fallback mechanisms.

# import requests

# def get_weather():
#     url = (
#         "https://api.open-meteo.com/v1/forecast"
#         "?latitude=12.97&longitude=77.59&current=temperature_2m"
#     )

#     # No timeout
#     # No retry
#     # No exception handling
#     # No fallback

#     response = requests.get(url)
#     data = response.json()

#     print("Temperature:", data["current"]["temperature_2m"], "°C")

# get_weather()

import time
import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=12.97&longitude=77.59&current=temperature_2m"
)

def get_weather():

    for attempt in range(3):  # Retry 3 times
        try:
            print(f"Attempt {attempt+1}")

            response = requests.get(URL, timeout=5)

            response.raise_for_status()

            data = response.json()

            temp = data["current"]["temperature_2m"]

            print("Temperature:", temp, "°C")

            return

        except Exception as e:
            print("Error:", e)

            if attempt < 2:
                print("Retrying...\n")
                time.sleep(2)

    print("\nUsing fallback...")
    print("Temperature: Not Available")

get_weather()