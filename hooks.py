from events import MessageObj as message

class Hook:
	''' Class for building hook objects to compare to event objects(MessageObj)'''

	def __init__(self, message, callback):
		self.message = message
		self.callback = callback
	
class Hooks:
	''' Class for managing hooks. adds hooks to the list and checks them '''

	hooks = []

	def add_hooks(self, hook):
		self.hooks.append(hook)

	def check_message(self):
		print("Received {}. Looping through hooks to find a match...").format(msg)
		for hook in self.hooks:
			if str.find(msg, hook.message) >=0:
				print("{0}  matches {1}, execute callback function.")
				hook.callback(msg)
			else:
			print("Message does not match")

	
	def check_modules(self):
		pass