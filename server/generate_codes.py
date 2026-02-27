import requests

# Generate codes on server
response = requests.post('http://localhost:5000/generate_codes', json={'count': 100})
print(response.json())