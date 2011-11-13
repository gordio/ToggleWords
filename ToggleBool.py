import sublime, sublime_plugin

bool_dict = [
	('true', 'false'),
	('yes', 'no'),
	('on', 'off'),
	('0', '1'),
	('left', 'right'),
	('top', 'bottom'),
	('up', 'down'),
	('width', 'height'),
]

class ToggleBoolCommand(sublime_plugin.TextCommand):
	def toggle_bool(self, view, region):
		word = self.view.substr(region)

		for bool_word in bool_dict:
			if word == bool_word[0]:
				self.view.replace(view, region, bool_word[1])
				return
			if word == bool_word[1]:
				self.view.replace(view, region, bool_word[0])
				return

			# For case when first letter is uppercase
			if word == bool_word[0].capitalize():
				self.view.replace(view, region, bool_word[1].capitalize())
				return
			if word == bool_word[1].capitalize():
				self.view.replace(view, region, bool_word[0].capitalize())
				return

			# For case when all letters are uppercase
			if word == bool_word[0].upper():
				self.view.replace(view, region, bool_word[1].upper())
				return
			if word == bool_word[1].upper():
				self.view.replace(view, region, bool_word[0].upper())
				return
				
		# Word not found? Show message
		sublime.status_message("ToggleBool: Can't find toggles for '%s'" % word)
		
	def run(self, view):
		for region in self.view.sel():
			word_region = self.view.word(region)
			self.toggle_bool(view, word_region)
