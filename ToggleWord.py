import sublime
import re
from sublime import Region
import sublime_plugin

PLUGIN_NAME = "ToggleWord"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"

DEFAULT_WORDS = [
	["true", "false"],
	["yes", "no"],
	["on", "off"],
	["0", "1"]
]

COMPLEX_WORD_PATTERN = "\W"

class ToggleWordCommand(sublime_plugin.TextCommand):

	def select_if_complex_word(self, view, new_word, old_region_begin, word_pattern=COMPLEX_WORD_PATTERN):
		containsWords = re.search(word_pattern,new_word)
		if containsWords != None:
			newWordRegion = Region(old_region_begin, old_region_begin + len(new_word))
			self.view.sel().add(newWordRegion)

	def toggle_word(self, view, region, words_dict=DEFAULT_WORDS, selected=True):
		editor_word = self.view.substr(region)

		# wordPattern = '\W'

		for word_item in words_dict:
			words_len = len(word_item)
			for i in range(0,words_len):
				# next item in array, or first item in array when end reached
				j = (i+1) % words_len
				# tRuE <> FalSe
				# For original case
				if editor_word == word_item[i]:
					self.view.replace(view, region, word_item[j])
					# select afterwards if new word contains a non alphanumeric symbol (for easy toggling)
					self.select_if_complex_word(view, word_item[j], region.a)
					return
				# true <> false
				# For case when all letters are lowercase
				if editor_word == word_item[i].lower():
					self.view.replace(view, region, word_item[j].lower())
					self.select_if_complex_word(view, word_item[j], region.a)
					return
				# True <> False
				# For case when first letter is uppercase
				if editor_word == word_item[i].capitalize():
					self.view.replace(view, region, word_item[j].capitalize())
					self.select_if_complex_word(view, word_item[j], region.a)
					return
				# TRUE <> FALSE
				# For case when all letters are uppercase
				if editor_word == word_item[i].upper():
					self.view.replace(view, region, word_item[j].upper())
					self.select_if_complex_word(view, word_item[j], region.a)
					return


		# Word not found? Show message
		sublime.status_message(
			"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
		)

	def run(self, view):

		# Would be nice to only run config when loading the editor,
		# not on each time the main function is called, but...
		# can't figure out how to do that without breaking the loading of plugin
		user_dict = sublime.Settings.get(sublime.load_settings(SETTINGS_FILE), 'toggle_word_dict', {})

		words_dict = DEFAULT_WORDS
		selected = False

		for item in user_dict:
			words_dict.append(item)

		for region in self.view.sel():
			if region.a != region.b:
				textRegion = region
				selected = True
			else:
				textRegion = self.view.word(region)
			self.toggle_word(view, textRegion, words_dict, selected)
