import requests
from bs4 import BeautifulSoup as bs
from os.path import basename

url = 'http://localhost:13579/variables.html'
def return_now_watching():
	soup = bs(requests.get(url).content)
	return '8:: I am now watching : 6{0} - {1} / {2} 8::'.format(
		basename(soup.find(id='filepath').string).replace('_', ' '),
		soup.find(id='positionstring').string,
		soup.find(id='durationstring').string
		)
