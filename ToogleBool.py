import sublime, sublime_plugin

bool_dict = [
	('true', 'false'),
	('on', 'off'),
	('yes', 'no'),
	('0', '1'),
	('+', '-'),
	('&', '|'),
	('&&', '||'),
	('<', '>'),
]

class ToggleBoolCommand(sublime_plugin.TextCommand):
	def run(self, view):
		word_region = self.view.word(self.view.sel()[0])
		word = self.view.substr(word_region)

		for bool_word in bool_dict:
			if word == bool_word[0]:
				self.view.replace(view, word_region, bool_word[1])
			if word == bool_word[1]:
				self.view.replace(view, word_region, bool_word[0])

