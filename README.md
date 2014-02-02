About
=====
Plugin for Sublime Text 3 - toggle "boolean" words with supporting user defined dictionary.

```
 true <-> false
  yes <-> no
   on <-> off
    0 <-> 1
 left <-> right
  top <-> bottom
   up <-> down
width <-> height
```

and this automatically understand

```
False <-> True
FALSE <-> TRUE
…
```


Usage
-----
Set cursor on word or select word and press <kbd>Cmd</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd> or <kbd>WinKey</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd> or <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd>


Installation
------------
0. Install Package Controll
1. <kbd>Shift</kbd>+<kbd>Control</kbd>+<kbd>P</kbd> type `Toggle` find Toggle Words end press <kbd>Enter</kbd>
2. Have fun!

or

1. Open you Sublime Text 2 Packages directory
2. Run `git clone git://github.com/gordio/ToggleBool`
3. Have fun!


Configure
---------

### Keys
Put this in you sublime-keymap `{"keys": ["alt+t"], "command": "toggle_bool" }`


### User defined dictionary
Example file `ToggleWord.sublime-settings`

```
{
	// User defined words
	"toggle_word_dict": {
		"left":	"right",
		"top":	"bottom",
		"up":	"down",
		"width": "height"
	}
}
```