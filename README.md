#About

Plugin for Sublime Text 3 - toggle words with support for user defined arrays.

```
 true -> false
  yes -> no
   on -> off
    0 -> 1
 left -> right
  top -> bottom
   up -> down
width -> height
```

and this automatically understand original words and ->

```
false <-> true
False <-> True
FALSE <-> TRUE
```

#Usage

Set cursor on word or select word and press <kbd>Cmd</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd> (OS X), <kbd>WinKey</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd> (Windows) or <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>x</kbd> (Linux).


#Installation

0. Install Package Control
1. Open ST command panel (<kbd>Shift</kbd>+<kbd>Control</kbd>+<kbd>P</kbd>), choose `Package Control — Install Package`, type `Toggle`, find Toggle Words end press <kbd>Enter</kbd>
2. Have fun!

or

1. Open you Sublime Text 3 Packages directory
2. Run `git clone git://github.com/gordio/ToggleWords`
3. Have fun!


#Configure

## Keys

You may redefine the key bindings in your sublime-keymap with command `toggle_word`.


## User defined arrays

You can define lists of words, which will be cycled through in order.

Example file `ToggleWords.sublime-settings`:

```
{
    // User defined words
    "toggle_word_dict": [
        ["left", "right"],
        ["top", "bottom"],
        ["up", "down"],
        ["width", "height"],
        ["red","orange","yellow","green","blue","purple"]
    ]
}
```

If installed using `Package Control` dictionary file should be located in `<data_path>/Packages`. To get there select `Preferences -> Browse Packages...` in Sublime menu. Create one if it does not exist.
