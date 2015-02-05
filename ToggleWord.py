import sublime
import re
from sublime import Region
import sublime_plugin

PLUGIN_NAME = "ToggleWord"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"


class ToggleWordCommand(sublime_plugin.TextCommand):

	def toggle_word(self, view, region, words_dict, selected=False, cursorPos=-1):
		editor_word = self.view.substr(region)

		for word_item in words_dict:
			words_len = len(word_item)
			word_item.sort(key=len, reverse=True)

			for i in range(0,words_len):
				# next item in array, or first item in array when end reached
				j = (i+1) % words_len
				# tRuE <> FalSe
				# For original case
				if editor_word == word_item[i]:
					self.view.replace(view, region, word_item[j])
					sublime.status_message("{0}, code 1: word under cursor '{1}' is equal to toggle '{2}', changed to next toggle '{3}'".format(PLUGIN_NAME, editor_word, word_item[i], word_item[j]))
					return
				# true <> false
				# For case when all letters are lowercase
				if editor_word == word_item[i].lower():
					self.view.replace(view, region, word_item[j].lower())
					sublime.status_message("{0}, code 2: word under cursor '{1}' is almost equal to lowercase toggle '{2}', changed to next toggle '{3}' (lowercased)".format(PLUGIN_NAME, editor_word, word_item[i], word_item[j]))
					return
				# True <> False
				# For case when first letter is uppercase
				if editor_word == word_item[i].capitalize():
					self.view.replace(view, region, word_item[j].capitalize())
					sublime.status_message("{0}, code 3: word under cursor '{1}' is almost equal to capitalized toggle '{2}', changed to next toggle '{3}' (capitalized)".format(PLUGIN_NAME, editor_word, word_item[i], word_item[j]))
					return
				# TRUE <> FALSE
				# For case when all letters are uppercase
				if editor_word == word_item[i].upper():
					self.view.replace(view, region, word_item[j].upper())
					sublime.status_message("{0}, code 4: word under cursor '{1}' is almost equal to uppercase toggle '{2}', changed to next toggle '{3}' (uppercased)".format(PLUGIN_NAME, editor_word, word_item[i], word_item[j]))
					return
				# if word under cursor CONTAINS one of the user words
				if word_item[i] in editor_word and selected == False:
					part_word_region = self.view.find(word_item[i], region.a, sublime.LITERAL)
					if part_word_region.a <= cursorPos <= part_word_region.b:
						self.view.replace(view, part_word_region, word_item[j])
						sublime.status_message(
							"{0}, code 5a: Word under cursor '{1}' contains toggle '{2}', changed to next toggle '{3}'".format(PLUGIN_NAME, editor_word, word_item[i], word_item[j])
						)
					else:
						sublime.status_message("{0}, code 5b: too many toggles in the word under cursor '{1}'. Searched from {2} to {3}, cursor at {4}".format(PLUGIN_NAME, editor_word,part_word_region.a,part_word_region.b,cursorPos))
					return
				# if user word spans across several words (or includes non word symbols) and cursor is within one of them
				lineRegion = self.view.line(region)
				userWordRegion = self.view.find(word_item[i], lineRegion.a, sublime.LITERAL)
				if userWordRegion.a <= cursorPos <= userWordRegion.b and selected == False:
					self.view.replace(view, userWordRegion, word_item[j])
					sublime.status_message(
						"{0}, code 6: Word '{1}' found from pos {2} to {3} on line beginning from pos {4}, cursor is at pos {5}. Toggled to '{6}'".format(PLUGIN_NAME, word_item[i], userWordRegion.a,userWordRegion.b,lineRegion.a,region.a, word_item[j])
					)
					return


		# Word not found? Show message
		sublime.status_message(
			"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
		)

	def run(self, view):

		# Would be nice to only run config when loading the editor,
		# not on each time the main function is called, but...
		# can't figure out how to do that without breaking the loading of plugin
		words_dict = sublime.Settings.get(sublime.load_settings(SETTINGS_FILE), 'toggle_word_dict', {})

		if bool(words_dict) == False: #if user dic is empty
			return

		selected = False

		for region in self.view.sel():
			if region.a != region.b:
				textRegion = region
				cursorPos = -1
				selected = True
			else:
				textRegion = self.view.word(region)
				cursorPos = region.a
			self.toggle_word(view, textRegion, words_dict, selected, cursorPos)
