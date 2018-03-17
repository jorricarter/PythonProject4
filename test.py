import urllib.parse
import requests
from pprint import pprint

# people_api = 'https://en.wikipedia.org/w/api.php?action=query&format=json&'
#
# name = input('name: ')
#
# url = people_api + urllib.parse.urlencode({'titles': name, 'prop': 'images'})
#
# print(url)
#
# json_data = requests.get(url).json()
#
# print(json_data)

# pprint(requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Albert+Einstein&prop=images').json())
print('https://en.wikipedia.org/w/api.php?action=queryaction=query&titles=Image:Albert+Einstein+as+a+child.jpg&prop=imageinfo&iiprop=url')