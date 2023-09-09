import requests
import  time 
from flask_jwt_extended import create_access_token


api_key = 'your_api_key'  # Replace with your actual API key
token = create_access_token(identity=api_key)

# Send 6 requests in quick succession
for i in range(6):
    response = requests.get(url)
    print(f"Request {i+1}: Status Code {response.status_code}")
    time.sleep(12)  # Sleep for 12 seconds (to make sure we don't hit the limit)

url = 'http://localhost:5000/api/upload'
headers = {'Authorization': 'Bearer ' + token}
files = {'image': ('example.jpg', open('example.jpg', 'rb'))}

response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:
    print("File uploaded successfully")
else:
    print("Failed to upload file")
