import sublime
import re
from sublime import Region
import sublime_plugin

PLUGIN_NAME = "ToggleWords"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"


class ToggleWordCommand(sublime_plugin.TextCommand):


	def toggle_word(self, view, region, words_dict, cursorPos=-1):
		editor_word = self.view.substr(region)
		toggle_groups = words_dict


		for toggle_group in toggle_groups:
			toggle_group_word_count = len(toggle_group)
			toggle_group.sort(key=len, reverse=True)

			for cur_word in range(0,toggle_group_word_count):
				
				next_word = (cur_word+1) % toggle_group_word_count

				if cursorPos != -1: #selected == false
					lineRegion = self.view.line(region)
					line = self.view.substr(lineRegion)
					lineBegin = lineRegion.a
					for line_finding in re.finditer(re.escape(toggle_group[cur_word]), line, flags=re.IGNORECASE):
						lf_a = line_finding.span()[0]
						lf_b = line_finding.span()[1]
						finding_region = Region(lineBegin + lf_a, lineBegin + lf_b)
						if finding_region.contains(cursorPos):
							editor_word = self.view.substr(finding_region)
							region = finding_region


				if editor_word == toggle_group[cur_word]:
					self.view.replace(view, region, toggle_group[next_word])
					return
				if editor_word == toggle_group[cur_word].lower():
					self.view.replace(view, region, toggle_group[next_word].lower())
					return
				if editor_word == toggle_group[cur_word].capitalize():
					self.view.replace(view, region, toggle_group[next_word].capitalize())
					return
				if editor_word == toggle_group[cur_word].upper():
					self.view.replace(view, region, toggle_group[next_word].upper())
					return


		# Word not found? Show message
		sublime.status_message(
			"{0}: Can't find toggles for '{1}'".format(PLUGIN_NAME, editor_word)
		)

	def run(self, view):

		# Would be nice to only run config when loading the editor,
		# not on each time the main function is called, but...
		# can't figure out how to do that without breaking the loading of plugin
		words_dict = sublime.Settings.get(sublime.load_settings(SETTINGS_FILE), 'toggle_words_dict', {})

		if bool(words_dict) == False: #if user dic is empty or does not exist
			return

		for region in self.view.sel():
			if region.a != region.b:
				textRegion = region
				cursorPos = -1
			else:
				textRegion = self.view.word(region)
				cursorPos = region.a
			self.toggle_word(view, textRegion, words_dict, cursorPos)
