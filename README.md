## Game of Life Kata

This script will read a text file [start.txt](start.txt) as a game state for the starting generation. The output will be printed to stdout and the main function will return `True`.

### Program
```python
$ python3 src/audition.py
```

### Tests
```python
$ python3 test/audition_test.py
```

### Coding Overview
I solved this problem in a few parts. The first part was to handle game state initialization. The code in [file_tools.py](src/file_tools.py) contains the logic necessary to parse a game state from a file. The text is read from the file according to the bounds indicated on line 2, and then the subsequent text is converted into a binary array or arrays (2D matrix). It wasn't required to convert the text to binary, but I felt it was a better representation of the actual data. This also allowed me avoid handling invalid test data while running generations. Rather, a `ValueError` will be raised in the event you provide a game state with invalid characters. The next part of this exercise was to apply the Game of Life algorithim. This can be found in [audition.py](src/audition.py). Here, the neighbors must be calculated, and then the next generation can be evaluated. Lastly, the output has to be converted back into ASCII for visual representation.

### Testing Overview
I used a method called Discovery Testing. If you know of Justin Searls, he has a great talk about this technique. You can also find some information on his company's Github: https://github.com/testdouble/contributing-tests/wiki/Discovery-Testing. Using this technique, I started to write functions that can be put into two categories:
1. Collaborator Functions - Functions that call other functions and orchestrate behavior of the code
2. Leaf Functions - Functions that do not call other functions but rather take a set of inputs, and return a result (pure function)
I used this technique heavily at Aver and I like it a lot. It does lend to write code in a very functional manner, but it makes refactoring and rewriting tests a breeze. However, one thing about this exercise is that you don't see any class definitions here. State is managed at a functional level, and this may not be the best solution. It's quite obvious in the code here that `bounds` and `game_state` are things that needs to be shared across a lot of functions in order to do their job. This is an indicator that an OOP approach would pull this state into an object which can be read and manipulated across other instance functions. I thought I'd mention this, since I know it's likely something you look for in these solutions, and I clearly didn't do that :D

Thanks for taking the time!