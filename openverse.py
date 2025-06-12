import requests

query = 'cat'
url = f'https://api.openverse.engineering/v1/images?q={query}&license=cc0&page_size=5'

response = requests.get(url)
data = response.json()

for result in data['results']:
    print(result['url'])  # Direct image link
