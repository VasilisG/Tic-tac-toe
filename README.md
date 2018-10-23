# Tic-tac-toe
A simple command line tic-tac-toe game made in Python.

It features a basic menu in which you can choose the difficulty level as well as the symbol character for your match.

As for the opponent, its moves are based on the [Minimax algorithm](https://en.wikipedia.org/wiki/Minimax#Pseudocode), having the following heuristic function:

* If the player has three in a row, column or diagonally, then Minimax returns 1.
* If the opponent has three in a row, column or diagonally, then Minimax returns -1.
* For every other case, Minimax returns 0.
