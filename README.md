# Tic-tac-toe
A simple command line tic-tac-toe game made in Python.

It features a basic menu in which you can choose the difficulty level as well as the symbol character for your match.

As for the opponent, its moves are based on the [Minimax algorithm](https://en.wikipedia.org/wiki/Minimax#Pseudocode), having the following heuristic function:

* If the player has three in a row, column or diagonally, then Minimax returns 1000.
* If the player has two in a row, column or diagonally, without opponent's presence, then Minimax returns 100.
* If the player has only one symbol in a row, column or diagonally, without an opponent's symbol, then Minimax returns 10. 
* If the player doesn't have any symbol in a row, column or diagonally, Minimax returns 1.

Same goes for the opponent, using negative values.
