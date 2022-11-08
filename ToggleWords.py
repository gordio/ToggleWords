import sublime
import re
from sublime import Region
import sublime_plugin

PLUGIN_NAME = "ToggleWords"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"


class ToggleWordCommand(sublime_plugin.TextCommand):
    # old logic (three or more words group)
    toggle_groups = []

    # normal dict for quick access
    full_toggle_groups = {}
    # inverted dict for quick access
    full_toggle_groups_invert = {}
    # cached keys for quick check
    words_group_set_1 = set()
    words_group_set_2 = set()

    def __init__(self, view):
        super().__init__(view)
        self.load_config()

    def load_config(self):
        print(f"{PLUGIN_NAME}: Loading config")
        sublime_settings = sublime.load_settings(SETTINGS_FILE)
        toggle_words_dict = sublime.Settings.get(sublime_settings, "toggle_words_dict", {})
        toggle_words_list = sublime.Settings.get(sublime_settings, "toggle_words_list", {}) or []

        # Pre compute some cache
        compiled_word_groups = {}
        for item in toggle_words_dict:
            try:
                w1, w2 = item
            except ValueError:
                toggle_words_list.append(item)
                continue
            compiled_word_groups[w1] = w2
            compiled_word_groups[w1.lower()] = w2.lower()
            compiled_word_groups[w1.capitalize()] = w2.capitalize()
            compiled_word_groups[w1.upper()] = w2.upper()

        # new boolean logic (improved performance)
        self.full_toggle_groups = compiled_word_groups
        self.full_toggle_groups_invert = dict(zip(compiled_word_groups.values(), compiled_word_groups.keys()))
        self.words_group_set_1 = set(compiled_word_groups.keys())
        self.words_group_set_2 = set(compiled_word_groups.values())

        # old cycle logic
        self.toggle_groups = toggle_words_list

    def run(self, view: sublime.View):
        # if user dic is empty show warning and do nothing
        if not self.full_toggle_groups and not self.toggle_groups:
            sublime.status_message("Words for toggle is not found in configuration.")
            return

        # cycle through all selected regions
        for region in self.view.sel():
            if region.a != region.b:
                text_region = region
                cursor_position = -1
            else:
                text_region = self.view.word(region)
                cursor_position = region.a

            success = self.toggle_word_quick_invert(view, text_region, cursor_position)
            if success:
                continue
            # if quick invert method is not give result
            success = self.toggle_word(view, text_region, cursor_position)
            if success:
                continue

    def toggle_word_quick_invert(self, view: sublime.View, region: sublime.Region, cursor_position=-1) -> bool:
        """Quick single word toggle"""
        editor_word = self.view.substr(region)
        if editor_word in self.words_group_set_1:
            self.view.replace(view, region, self.full_toggle_groups[editor_word])
        elif editor_word in self.words_group_set_2:
            self.view.replace(view, region, self.full_toggle_groups_invert[editor_word])
        else:
            return False
        return True

    def toggle_word(self, view: sublime.View, region: sublime.Region, cursor_position=-1) -> bool:
        editor_word = self.view.substr(region)

        for toggle_group in self.toggle_groups:
            toggle_group_word_count = len(toggle_group)
            # toggle_group.sort(key=len, reverse=True)

            for cur_word in range(0, toggle_group_word_count):
                next_word = (cur_word + 1) % toggle_group_word_count

                if cursor_position != -1:  # selected == false
                    lineRegion = self.view.line(region)
                    line = self.view.substr(lineRegion)
                    lineBegin = lineRegion.a

                    re_iter = re.finditer(re.escape(toggle_group[cur_word]), line, flags=re.IGNORECASE)
                    for line_finding in re_iter:
                        lf_a = line_finding.span()[0]
                        lf_b = line_finding.span()[1]
                        finding_region = Region(lineBegin + lf_a, lineBegin + lf_b)
                        if finding_region.contains(cursor_position):
                            editor_word = self.view.substr(finding_region)
                            region = finding_region

                if editor_word == toggle_group[cur_word]:
                    self.view.replace(view, region, toggle_group[next_word])
                elif editor_word == toggle_group[cur_word].lower():
                    self.view.replace(view, region, toggle_group[next_word].lower())
                elif editor_word == toggle_group[cur_word].capitalize():
                    self.view.replace(view, region, toggle_group[next_word].capitalize())
                elif editor_word == toggle_group[cur_word].upper():
                    self.view.replace(view, region, toggle_group[next_word].upper())
                else:
                    continue
                return True

        # Word not found? Show message
        sublime.status_message(f"{PLUGIN_NAME}: Can't find toggles for '{editor_word}'")
        return False
