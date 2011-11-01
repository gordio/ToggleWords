# About
Sublime Text 2 Plugin - toggle boolean words

```
false <-> true
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
_TODO_


# Configure

### Keys
Put this in you sublime-keymap ```"keys": ["alt+t"], "command": "toggle_bool" }```

### Words
_TODO_


# TODO
- Work for multi words selection
- Зациклить перебор в словаре, что бы работало для ('true', 'false', 'nil') переключая true => false => nil => true...