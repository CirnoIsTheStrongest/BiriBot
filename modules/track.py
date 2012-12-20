import requests
from xml.etree import ElementTree
import re

# EG200546216JP
# http://www.packagetrackr.com/track/550487484564

class TrackPackages():
	def __init__(self):
		self.base_url = 'http://www.boxoh.com/?rss=1&t=+'

	def track_package(self, tracking_number):
		tracking_data = requests.get(self.base_url+tracking_number)
		track_xml = ElementTree.fromstring(tracking_data.text)
		title = track_xml.find('.//channel')
		item = title.find('item')
		return re.sub('<[^<]+?>', ' ', item.find('description').text)