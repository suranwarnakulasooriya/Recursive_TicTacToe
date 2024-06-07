# Recursive TicTacToe
A pygame-based program that runs tic tac toe recursively at an arbitrary depth.

## Dependencies
Python can be downloaded from [python.org](https://www.python.org/downloads/) and `pygame` can be installed with `pip`:
```
pip install pygame
```

## Arguments
All of the following arguments are optional:
|Alias|Name|Description|Default|Range|
|------------|----|-----------|-------|-----|
|-d|--depth|game recursion depth|7|at least 1, be caucious of going over 5|
|-a|--autoplay|have the game play itself|off|
|-s|--size|screen side length in pixels|800|min 100|

For example:
```
python3.10 recursive_tictactoe.py -d 3 --autoplay -s 500 # depth of 3 with autoplay and screen size 500
```

## Controls
|Key|Action|
|---|------|
|q/ctrl+C/esc|exit|
|click|place X or O|
|r|restart|
