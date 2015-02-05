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

	def preselect_if_next_is_complex_word(self, view, new_word, old_region_begin, word_pattern=COMPLEX_WORD_PATTERN):
		containsWords = re.search(word_pattern,new_word)
		if containsWords != None:
			newWordRegion = Region(old_region_begin, old_region_begin + len(new_word))
			self.view.sel().add(newWordRegion)

	def toggle_word(self, view, region, words_dict=DEFAULT_WORDS, selected=False):
		editor_word = self.view.substr(region)

		# wordPattern = '\W'

		for word_item in words_dict:
			words_len = len(word_item)
			for i in range(0,words_len):
				# next item in array, or first item in array when end reached
				j = (i+1) % words_len
				hasWordUnderCursor = re.search(word_item[i],editor_word)
				# tRuE <> FalSe
				# For original case
				if editor_word == word_item[i]:
					self.view.replace(view, region, word_item[j])
					# select afterwards if new word contains a non alphanumeric symbol (for easy toggling)
					self.preselect_if_next_is_complex_word(view, word_item[j], region.a)
					sublime.status_message('1')
					return
				# true <> false
				# For case when all letters are lowercase
				if editor_word == word_item[i].lower():
					self.view.replace(view, region, word_item[j].lower())
					self.preselect_if_next_is_complex_word(view, word_item[j], region.a)
					sublime.status_message('2')
					return
				# True <> False
				# For case when first letter is uppercase
				if editor_word == word_item[i].capitalize():
					self.view.replace(view, region, word_item[j].capitalize())
					self.preselect_if_next_is_complex_word(view, word_item[j], region.a)
					sublime.status_message('3')
					return
				# TRUE <> FALSE
				# For case when all letters are uppercase
				if editor_word == word_item[i].upper():
					self.view.replace(view, region, word_item[j].upper())
					self.preselect_if_next_is_complex_word(view, word_item[j], region.a)
					sublime.status_message('4')
					return
				# if word under cursor CONTAINS one of the user words
				if word_item[i] in editor_word and selected == False:
					part_word_region = self.view.find(word_item[i], region.a)
					self.view.replace(view, part_word_region, word_item[j])
					self.preselect_if_next_is_complex_word(view, word_item[j], part_word_region.a)
					sublime.status_message(
						"5: Word '{0}' found in {1}, replaced region is {2}".format(editor_word, word_item[i],self.view.substr(part_word_region))
					)
					return
				# if user word consists of several words and cursor is within one of them
				# if word_item[i] in editor_word and selected == False:
				cursorRegion = self.view.sel()[0]
				lineRegion = self.view.line(region)
				userWordRegion = self.view.find(word_item[i], lineRegion.a, sublime.LITERAL)
				if userWordRegion.a != -1:
					sublime.status_message(
						"6: Word '{0}' found from pos {1} to {2} on line {3}, cursor is at {4}".format(word_item[i], userWordRegion.a,userWordRegion.b,lineRegion.a,region.a)
					)
				if userWordRegion.a < cursorRegion.a < userWordRegion.b and selected == False:
					self.view.replace(view, userWordRegion, word_item[j])
					# self.preselect_if_next_is_complex_word(view, word_item[j], part_word_region.a)
					return
				# else:
				# sublime.status_message(
				# 	"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
				# )


		# Word not found? Show message
		# sublime.status_message(
		# 	"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
		# )

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
