import sublime
import sublime_plugin

PLUGIN_NAME = "ToggleWord"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"

DEFAULT_WORDS = [
	["true", "false"],
	["yes", "no"],
	["on", "off"],
	["0", "1"]
]

# Only run config when loading the editor, not on each time the main function is called...
user_dict = sublime.Settings.get(sublime.load_settings(SETTINGS_FILE), 'toggle_word_dict', {})

words_dict = DEFAULT_WORDS

for item in user_dict:
	words_dict.append(item)

class ToggleWordCommand(sublime_plugin.TextCommand):

	def toggle_word(self, view, region, words_dict=DEFAULT_WORDS):
		editor_word = self.view.substr(region)

		for word_item in words_dict:
			words_len = len(word_item)
			for i in range(0,words_len):
				# next item in array, or first item in array when end reached
				j = (i+1) % words_len
				# tRuE <> FalSe
				# For original case
				if editor_word == word_item[i]:
					self.view.replace(view, region, word_item[j])
					return
				# true <> false
				# For case when all letters are lowercase
				if editor_word == word_item[i].lower():
					self.view.replace(view, region, word_item[j].lower())
					return
				# True <> False
				# For case when first letter is uppercase
				if editor_word == word_item[i].capitalize():
					self.view.replace(view, region, word_item[j].capitalize())
					return
				# TRUE <> FALSE
				# For case when all letters are uppercase
				if editor_word == word_item[i].upper():
					self.view.replace(view, region, word_item[j].upper())
					return

		# Word not found? Show message
		sublime.status_message(
			"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
		)

	def run(self, view):

		for region in self.view.sel():
			word_region = self.view.word(region)
			self.toggle_word(view, word_region, words_dict)
