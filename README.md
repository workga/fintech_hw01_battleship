# Battleship game
This is a simple console implementation of the Battleship game using Curses and Typer modules.

### Features
- Takes two parameters - the height and the width of the field.
  The default field size is 10x10.
- Automatically saves the unfinished game for each field size.
- Allows you to change the size of the console and asks you to increase its size if necessary.

### Requirements
- click==8.0.4
- typer==0.4.0

### Usage
Run with default parameters:
```bash
python battleship
```

Run with given parameters:
```bash
python battleship 20 20
```

And even so:
```bash
python battleship 20
```

Using debug mode:
```bash
python battleship --debug
```
```bash
python battleship --debug 20 20
```

### Control
| Key      | Action      |
| -------- | ----------- |
| [q]      | quit        |
| [arrows] | move cursor |
| [space]  | drop bomb   |

