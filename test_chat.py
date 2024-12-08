import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "Hello"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
except Exception as e:
    print(f"Error while making the request: {e}")
