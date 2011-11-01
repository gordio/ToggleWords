# About
Sublime Text 2 Plugin - toggle boolean words

```
 true <-> false
  yes <-> no
   on <-> off
    0 <-> 1
    + <-> -
   || <-> &&
    | <-> &
    < <-> >
```

and this automatic understand

```
False <-> True
FALSE <-> TRUE
# ... etc
```


# Usage
Set cursor on word or select word and press Super+Alt+x


# Installation
1. Open you Sublime Text 2 Packages directory
2. Run `git clone git://github.com/gordio/ToggleBool`
3. Have fun!


# Configure

### Keys
Put this in you sublime-keymap `"keys": ["alt+t"], "command": "toggle_bool" }`

### Words
_TODO_


# TODO
- Work for multi words selection
- Зациклить перебор в словаре, что бы работало для ('true', 'false', 'nil') переключая true => false => nil => true...
- Add user words
- Understand and +/- int values (lowest)
