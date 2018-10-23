import sys

class Node:

    score = {"0" : 1, "1" : 10, "2" : 100, "3" : 1000}

    def __init__(self, matrix, hValue, symbol, opponentSymbol):
        self.matrix = matrix
        self.hValue = hValue
        self.symbol = symbol
        self.opponentSymbol = opponentSymbol
        self.x = 0
        self.y = 0
        self.bestChild = None

    def __str__(self):
        return "Matrix: " + str(self.matrix) + ", Heuristic value: " + str(self.hValue) + ", Symbol: " + self.symbol

    def getMatrix(self):
        return self.matrix

    def getPosition(self, x, y):
        return self.matrix[x][y]

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getHValue(self):
        return self.hValue

    def setHValue(self, hValue):
        self.hValue = hValue

    def getSymbol(self):
        return self.symbol

    def getOpponentSymbol(self):
        return self.opponentSymbol

    def getBestChild(self):
        return self.bestChild

    def setBestChild(self, bestChild):
        self.bestChild = bestChild

    def generateChildren(self, maximizingPlayer):
        emptyTiles = []
        children = []
        length = len(self.matrix)

        for i in range(length):
            for j in range(length):
                if self.matrix[i][j] == " ":
                    emptyTiles.append((i,j))
        
        for tile in emptyTiles:
            matrix = [[self.matrix[i][j] for j in range(3)] for i in range(3)]
            if maximizingPlayer:
                matrix[tile[0]][tile[1]] = self.symbol
            else:
                matrix[tile[0]][tile[1]] = self.opponentSymbol

            self.setPosition(tile[0],tile[1])
            hValue = 0

            for row in matrix:
                if row.count(self.symbol)==3:
                    children.append(Node(matrix, 1, self.opponentSymbol, self.symbol))
                    break
                if row.count(self.opponentSymbol)==3:
                    children.append(Node(matrix, -1, self.opponentSymbol, self.symbol))
                    break

            for i in range(3):
                if [matrix[0][i], matrix[1][i], matrix[2][i]].count(self.symbol)==3:
                    children.append(Node(matrix, -1, self.opponentSymbol, self.symbol))
                    break
                if [matrix[0][i], matrix[1][i], matrix[2][i]].count(self.opponentSymbol)==3:
                    children.append(Node(matrix, -1, self.opponentSymbol, self.symbol))
                    break

            if [matrix[0][0], matrix[1][1], matrix[2][2]].count(self.symbol)==3:
                children.append(Node(matrix, 1, self.opponentSymbol, self.symbol))
            elif [matrix[2][0], matrix[1][1], matrix[0][2]].count(self.symbol)==3:
                children.append(Node(matrix, 1, self.opponentSymbol, self.symbol))

            elif [matrix[0][0], matrix[1][1], matrix[2][2]].count(self.opponentSymbol)==3:
                children.append(Node(matrix, -1, self.opponentSymbol, self.symbol))
            elif [matrix[2][0], matrix[1][1], matrix[0][2]].count(self.opponentSymbol)==3:
                children.append(Node(matrix, -1, self.opponentSymbol, self.symbol))

            else:
                # children.append(Node(matrix, 0, self.opponentSymbol, self.symbol))
                children.append(Node(matrix, 0, self.symbol, self.opponentSymbol))

        return children


class Player:

    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol

    def __str__(self):
        return "Player symbol: " + self.symbol

    def isValid(self, x, y):
        return x>=0 and x<3 and y>=0 and y<3 and self.game.getPosition(x,y)==' '

    def makeMove(self):
        while True:
            x = int(input("Enter x position [0 to 2]: "))
            y = int(input("Enter y position [0 to 2]: "))
        
            try:
                if self.isValid(x,y):
                    self.game.updateMatrix(x, y, self.symbol)
                    self.game.showMatrix()
                    print()
                    return
                else:
                    print("\nInvalid coordinates, please try again.\n")
            except ValueError:
                print("\nInvalid input (non integer). Please try again.\n")

    def getSymbol(self):
        return self.symbol


class Opponent:

    diff = {"easy" : 1, "medium" : 2, "hard" : 3}

    def __init__(self, game, symbol, opponentSymbol, difficulty):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = opponentSymbol
        self.depth = Opponent.diff[difficulty]

    def __str__(self):
        return "Opponent's symbol: " + self.symbol + ", " + "Difficulty (depth): " + self.depth 

    def getSymbol(self):
        return self.symbol

    def getOpponentSymbol(self):
        return self.opponentSymbol

    def bestMove(self, node, depth, maximizingPlayer):
        children = []
        nodeValue = node.getHValue()

        if nodeValue==1 or nodeValue==-1:
            return nodeValue, node
        else: 
            children = node.generateChildren(maximizingPlayer)

            if depth==0 or len(children)==0:
                return node.getHValue(), node

            if maximizingPlayer:
                bestValue = -10
                bestNode = Node(None, bestValue, self.symbol, self.opponentSymbol)
                for child in children:
                    tempValue, tempNode = self.bestMove(child, depth-1, False)
                    bestValue = max([bestValue, tempValue])
                    if bestValue == tempNode.getHValue():
                        bestNode = tempNode
                node.setHValue(bestValue)
                node.setBestChild(bestNode)
                return bestValue, node

            else:
                bestValue = 10
                bestNode = Node(None, bestValue, self.symbol, self.opponentSymbol)
                for child in children:
                    tempValue, tempNode = self.bestMove(child, depth-1, True)
                    bestValue = min([bestValue, tempValue])
                    if bestValue == tempNode.getHValue():
                        bestNode = tempNode
                node.setHValue(bestValue)
                node.setBestChild(bestNode)
                return bestValue, node

    def makeMove(self):
        node = Node(self.game.getMatrix(), 0, self.symbol, self.opponentSymbol)
        depth = self.depth
        value, node = self.bestMove(node, depth, True)
        return node.getBestChild().getMatrix()

class Game:

    def __init__(self):
        self.rounds = 1
        self.matrix = [[" " for i in range(3)] for j in range(3)]

    def getRounds(self):
        return self.rounds

    def incrementRounds(self):
        self.rounds += 1

    def getMatrix(self):
        return self.matrix

    def setMatrix(self, matrix):
        self.matrix = matrix

    def update(self, matrix):
        self.matrix = matrix

    def updateMatrix(self, x, y, symbol):
        self.matrix[x][y] = symbol

    def getPosition(self, x, y):
        return self.matrix[x][y]

    def symbolWon(self, symbol):
        for row in self.matrix:
            if row.count(symbol) == 3:
                return True
        for i in range(3):
            if [self.matrix[0][i], self.matrix[1][i], self.matrix[2][i]].count(symbol)==3:
                return True
        if [self.matrix[0][0], self.matrix[1][1], self.matrix[2][2]].count(symbol)==3:
            return True
        if [self.matrix[2][0], self.matrix[1][1], self.matrix[0][2]].count(symbol)==3:
            return True
        return False

    def peerWon(self, peer):
        return self.symbolWon(peer.getSymbol())

    def isDraw(self):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j]==' ':
                    return False
        return True

    def showMatrix(self):
        length = len(self.getMatrix())
        print()
        print("-" * 13)
        for x in range(length):
            for y in range(length):
                print("|", end=" ")
                print(self.getPosition(x,y), end=" ")
            print("|")
            print("-" * 13)
        print()

    def showMessage(self, wonString):
        print(wonString)
        print("Total rounds: ", self.getRounds())


class TicTacToe:

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def __init__(self):
        self.player = None
        self.firstOpponent = None
        self.secondOpponent = None
        self.game = None

    def opponentMove(self, opponent):
        matrix = opponent.makeMove()
        self.game.update(matrix)
        self.game.showMatrix()


    def PlayerVsCpu(self, playerSymbol, opponentSymbol, opponentDifficulty):
        self.game = Game()
        self.player = Player(self.game, playerSymbol)
        self.firstOpponent = Opponent(self.game, opponentSymbol, playerSymbol, opponentDifficulty)
        self.game.showMatrix()

        while True:
            print("YOUR MOVE: ")
            self.player.makeMove()
            print()
            if self.game.peerWon(self.player):
                self.game.showMessage("You won!!")
                break

            if self.game.isDraw():
                self.game.showMessage("Game ended in draw.")
                break

            print("CPU MOVE: ")
            self.opponentMove(self.firstOpponent)
            print()
            if self.game.peerWon(self.firstOpponent):
                self.game.showMessage("CPU-1 won!!")
                break

            if self.game.isDraw():
                self.game.showMessage("Game ended in draw.")
                break

            self.game.incrementRounds()
            print()


class Program:

    def validate(self, diffLevel, validChoices):
        return diffLevel in validChoices

    def getDifficulty(self):
        difficulty = ''
        while True:
            print("\nChoose difficulty level:")
            print("1. EASY")
            print("2. MEDIUM")
            print("3. HARD")
            difficultyLevel = int(input("\nLevel [choose 1, 2 or 3]: "))
            if self.validate(difficultyLevel, [1,2,3]):
                if difficultyLevel==1:
                    difficulty = TicTacToe.EASY
                elif difficultyLevel==2:
                    difficulty = TicTacToe.MEDIUM
                else:
                    difficulty = TicTacToe.HARD
                return difficulty
            print("\nInvalid input. Please try again.\n")

    def getSymbols(self):
        symbol = ''
        opponentSymbol = ''
        while True:
            print("\nChoose player symbol: ")
            print("1. X")
            print("2. O")
            symbol = str(input("\nSymbol [type X or O]: "))
            if self.validate(symbol, ['x', 'X', 'o', 'O']):
                if symbol=='x' or symbol=='X':
                    opponentSymbol = 'O'
                else:
                    opponentSymbol = 'X'
                return (symbol, opponentSymbol)
            print("\nInvalid input. Please try again.\n")

    def askForMatchReplay(self):
        while True:
            answer = str(input("\nDo you want to replay that match? (Y/N): "))
            if answer.lower()=='y':
                return True
            elif answer.lower()=='n':
                return False
            else:
                print("\nInvalid input. Please try again.\n")
        print()

    def askToQuit(self):
        while True:
            print("\nWhat do you want to do?")
            print("1. Main menu")
            print("2. Quit")
            answer = int(input("\nEnter choice [1 or 2]: "))
            if self.validate(answer, [1,2]):
                return answer
            print("\nInvalid input. Please try again.\n")

    def showTitle(self):
        print()
        print("###################")
        print("### TIC-TAC-TOE ###")
        print("###################")
        print()

    def run(self):
        tictactoe = TicTacToe()
        self.showTitle()
        while True:
            difficulty = self.getDifficulty()
            symbols = self.getSymbols()
            while True:
                while True:
                    tictactoe.PlayerVsCpu(symbols[0], symbols[1], difficulty)
                    replay = self.askForMatchReplay()
                    if not replay:
                        break
                quit = self.askToQuit()
                if quit==1:
                    break
                else:
                    return

########################################################################################

if __name__ == '__main__':
    program = Program()
    program.run()