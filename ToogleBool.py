import sublime, sublime_plugin

bool_dict = [
	('true', 'false'),
	('yes', 'no'),
	('on', 'off'),
	('0', '1'),
	('+', '-'),
	('&', '|'),
	('&&', '||'),
	('<', '>'),
]

class ToggleBoolCommand(sublime_plugin.TextCommand):
	def ToggleBool(self, region):
		word = self.view.substr(region)

		for bool_word in bool_dict:
			if word == bool_word[0]:
				self.view.replace(view, word_region, bool_word[1])
				continue
			if word == bool_word[1]:
				self.view.replace(view, word_region, bool_word[0])
				continue

			# For first letter apper
			if word == bool_word[0].capitalize():
				self.view.replace(view, word_region, bool_word[1].capitalize())
				continue
			if word == bool_word[1].capitalize():
				self.view.replace(view, word_region, bool_word[0].capitalize())
				continue

			# For all letter's apper
			if word == bool_word[0].upper():
				self.view.replace(view, word_region, bool_word[1].upper())
				continue
			if word == bool_word[1].upper():
				self.view.replace(view, word_region, bool_word[0].upper())
				continue
		

	def run(self, view):
		for region in self.view.sel():
			word_region = self.view.word(region)
			self.ToggleBool(word_region)

