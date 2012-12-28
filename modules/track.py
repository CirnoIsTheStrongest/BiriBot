import requests
import bs4
# EG200546216JP
# http://www.packagetrackr.com/track/550487484564

class TrackPackages():
	def __init__(self):
		self.base_url = 'http://www.packagetrackr.com/track/'

	def track_package(self, tracking_number):
		return bs4.BeautifulSoup(requests.get(self.base_url+tracking_number).content).find("meta", {"name":"description"})['content']
		# soup = bs4.BeautifulSoup(tracking_data.content)
		# location = soup.find("meta", {"name":"description"})['content']
		# return location
		# track_xml = ElementTree.fromstring(tracking_data.text)
		# title = track_xml.find('.//channel')
		# item = title.find('item')
		# return re.sub('<[^<]+?>', ' ', item.find('description').text)