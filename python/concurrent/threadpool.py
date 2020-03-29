import requests
from concurrent.futures import ThreadPoolExecutor

urls = ['https://google.com', 'https://yahoo.com', 'https://bing.com', 'https://amazon.com']


with ThreadPoolExecutor(max_workers=4) as executor:
    result = executor.map(lambda url: requests.get(url).content, urls)

