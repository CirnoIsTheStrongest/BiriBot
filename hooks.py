from events import MessageObj

class Hook:
	''' Class for building hook objects to compare to event objects(MessageObj)'''

	def __init__(self, event_type, payload, callback):
		self.type = event_type
		self.payload = payload
		self.callback = callback
	
class Hooks:
	''' Class for managing hooks. adds hooks to the list and checks them '''

	def add_hooks(self):
		pass

	def check_internal(self):
		pass
	
	def check_message(self):
		pass
	
	def check_modules(self):
		pass