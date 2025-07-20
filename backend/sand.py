import requests

url = "https://app.ribbon.ai/be-api/v1/interviews"

headers = {
    "accept": "application/json",
    "authorization": "Bearer 6d9873d2-1cb3-4204-b2e4-cee7a91f2286"
}

response = requests.get(url, headers=headers)

print(response.text)