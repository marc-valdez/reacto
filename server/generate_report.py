import requests

# Output results from the server
response = requests.get('http://localhost:5000/export_csv')
with open('exported_results.csv', 'w', encoding='utf-8') as file:
    file.write(response.text)
print("CSV file saved as 'exported_results.csv'")
