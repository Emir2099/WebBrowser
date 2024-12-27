import requests

def fetch_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "<h1>Error loading page</h1>"
