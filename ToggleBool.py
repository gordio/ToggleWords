import sublime, sublime_plugin

bool_dict = [
	('true', 'false'),
	('yes', 'no'),
	('on', 'off'),
	('0', '1')
]

class ToggleBoolCommand(sublime_plugin.TextCommand):
	def toggle_bool(self, view, region):
		word = self.view.substr(region)
		found = False

		for bool_word in bool_dict:
			if word == bool_word[0]:
				found = True
				self.view.replace(view, region, bool_word[1])
				continue
			if word == bool_word[1]:
				found = True
				self.view.replace(view, region, bool_word[0])
				continue

			# For case when first letter is uppercase
			if word == bool_word[0].capitalize():
				found = True
				self.view.replace(view, region, bool_word[1].capitalize())
				continue
			if word == bool_word[1].capitalize():
				found = True
				self.view.replace(view, region, bool_word[0].capitalize())
				continue

			# For case when all letters are uppercase
			if word == bool_word[0].upper():
				found = True
				self.view.replace(view, region, bool_word[1].upper())
				continue
			if word == bool_word[1].upper():
				found = True
				self.view.replace(view, region, bool_word[0].upper())
				continue

		# Word not found?
		if found == False:
			sublime.status_message("ToggleBool: Can't find toggles for '%s'" % word)

	def run(self, view):
		for region in self.view.sel():
			word_region = self.view.word(region)
			self.toggle_bool(view, word_region)
