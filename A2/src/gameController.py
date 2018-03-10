
from constants import Constants
from board import Board
from evaluate import Evaluate
from gamePlay import minimax, alphaBeta

_print = print
def print(*args, **kwargs):
    kwargs['flush'] = True
    return _print(*args, **kwargs)

class Game():
    """
    Class to control The Dragon Queen game.
    """
    ply = None
    player = None
    board = None
    successors = None

    def __init__(self, depth_limit):
        """
        Constructor that initializes a board and starts a game.
        """
        self.ply = 0
        self.player = Constants.MAX
        self.board = Board()
        self.board.initialValues()
        self.successors = self.board.successors(self.player)
        self.depth_limit = depth_limit

    def isAtEndGame(self):
        return len(self.successors) == 0 or\
            Evaluate(self.board).utility(self.ply) != Constants.NON_TERMINAL

    def advanceWithAI(self, search):
        if self.isAtEndGame():
            return
        moves = self.successors
        minimum = Constants.INF
        maximum = Constants.NEGINF
        opponent = Constants.MIN if self.player == Constants.MAX else\
            Constants.MAX
        for i in moves:
            # Utility values for opponent's moves:
            util = search(i, self.player, self.ply + 1, self.depth_limit)
            if util > maximum:
                maxMove = i
                maximum = util
            elif util < minimum:
                minMove = i
                minimum = util
            if Evaluate(i).utility(self.ply) == Constants.INF:
                maxMove = i
                maximum = Constants.INF
            elif Evaluate(i).utility(self.ply) == Constants.NEGINF:
                minMove = i
                minimum = Constants.NEGINF

        # Update Game:
        self.board = maxMove if self.player == Constants.MAX else minMove
        self.ply += 1
        self.player = opponent
        self.successors = self.board.successors(self.player)

    def advanceWithPerson(self):
        pass

def runGame(depth_limit, search):
    game = Game(depth_limit)
    while not game.isAtEndGame():
        print("Current Board at ply: " + str(game.ply), "; Player:", game.player)
        print(game.board)
        #print("Advance?\n>")
        game.advanceWithAI(search)
    print("Final State:")
    print(game.board)

