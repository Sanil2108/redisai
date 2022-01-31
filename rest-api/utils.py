import requests

def download_image_data(url):
    response = requests.request("GET", url, headers={}, data={})
    return response.content
