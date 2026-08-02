#fallback pattern


# import requests

# url = "https://invalid-api.com/weather"

# response = requests.get(url)
# response.raise_for_status()

# print(response.json())

import requests

PRIMARY_API = "https://invalid-api.com/weather"

BACKUP_API = "https://jsonplaceholder.typicode.com/todos/1"

try:
    print("Calling Primary API...")

    response = requests.get(PRIMARY_API, timeout=3)
    response.raise_for_status()

    print("Primary API Response:")
    print(response.json())

except Exception:
    print("Primary API Failed!")
    print("Switching to Backup API...\n")

    response = requests.get(BACKUP_API, timeout=3)

    print("Backup API Response:")
    print(response.json())