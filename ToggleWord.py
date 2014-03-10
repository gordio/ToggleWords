import sublime
import sublime_plugin


PLUGIN_NAME = "ToggleWord"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"

DEFAULT_WORDS = [
	("true", "false"),
	("yes", "no"),
	("on", "off"),
	("0", "1")
]


class ToggleBoolCommand(sublime_plugin.TextCommand):

	def toggle_bool(self, view, region, words_dict=DEFAULT_WORDS):
		editor_word = self.view.substr(region)

		for word_item in words_dict:
			# PhantomJS <> Chrome
			# For case when letter cases are mixed
			# Words defined in the dictionary surrounded with "{{ }}" are
			# replaced as they are, without modifying their case
			if word_item[0].startswith('{{') and word_item[0].endswith('}}'):
				stripped_word = word_item[0].strip('{}');
				if editor_word == stripped_word:
					self.view.replace(view, region, word_item[1].strip('{}'))
					return
			if word_item[1].startswith('{{') and word_item[1].endswith('}}'):
				stripped_word = word_item[1].strip('{}');
				if editor_word == stripped_word:
					self.view.replace(view, region, word_item[0].strip('{}'))
					return

			# true <> false
			# For case when all letters are lowercase
			if editor_word == word_item[0].lower():
				self.view.replace(view, region, word_item[1].lower())
				return
			if editor_word == word_item[1].lower():
				self.view.replace(view, region, word_item[0].lower())
				return

			# True <> False
			# For case when first letter is uppercase
			if editor_word == word_item[0].capitalize():
				self.view.replace(view, region, word_item[1].capitalize())
				return
			if editor_word == word_item[1].capitalize():
				self.view.replace(view, region, word_item[0].capitalize())
				return

			# TRUE <> FALSE
			# For case when all letters are uppercase
			if editor_word == word_item[0].upper():
				self.view.replace(view, region, word_item[1].upper())
				return
			if editor_word == word_item[1].upper():
				self.view.replace(view, region, word_item[0].upper())
				return

		# Word not found? Show message
		sublime.status_message(
			"{0}: Can't find toggles for '{1}'".format(
				PLUGIN_NAME, editor_word))


	def run(self, view):
		# Why list? I still need two words
		# TODO: cycle words in array
		user_dict = sublime.Settings.get(
			sublime.load_settings(SETTINGS_FILE), 'toggle_word_dict', {})

		words_dict = DEFAULT_WORDS

		for item in user_dict.items():
			words_dict.append(item)

		for region in self.view.sel():
			word_region = self.view.word(region)
			self.toggle_bool(view, word_region, words_dict)
