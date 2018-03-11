
from constants import Constants
from board import Board, Piece
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
        self.player = Constants.MIN
        self.board = Board()
        self.board.initialValues()
        self.successors = self.board.successors(self.player)
        self.depth_limit = depth_limit

    def isAtEndGame(self):
        """
        Determine whether the current board is the end of the game.
        :return: True if at end, False otherwise
        """
        return len(self.successors) == 0 or\
            Evaluate(self.board).utility(self.ply) != Constants.NON_TERMINAL

    def advanceWithAI(self, search):
        """
        Advance the game to the new ply using AI.
        :param search: the search strategy to be used
        """
        if self.isAtEndGame():
            return
        moves = self.successors
        minimum = Constants.INF
        maximum = Constants.NEGINF
        opponent = Constants.MIN if self.player == Constants.MAX else\
            Constants.MAX
        maxMove = self.successors[0]
        minMove = self.successors[0]
        for i in moves:
            # Utility values for opponent's moves:
            heuristic = search(i, opponent, self.ply + 1, self.depth_limit)
            if(heuristic > Constants.INF and heuristic < Constants.NEGINF):
                print(i)
                assert(False)
            if heuristic > maximum:
                maxMove = i
                maximum = heuristic
            elif heuristic < minimum:
                minMove = i
                minimum = heuristic
            if Evaluate(i).utility(self.ply) >= Constants.INF:
                maxMove = i
                maximum = Constants.INF
            elif Evaluate(i).utility(self.ply) <= Constants.NEGINF:
                minMove = i
                minimum = Constants.NEGINF

        # Update Game:
        self.board = maxMove if self.player == Constants.MAX else minMove
        self.ply += 1
        self.player = opponent
        self.successors = self.board.successors(self.player)

    def parseMoveFromLine(self, line):
        """
        Parse chosen player moves from the given line.
        :param line: player's moves from command line
        """
        coords = line.split()
        coord_nums = []
        if len(coords) != 3 or coords[0] not in Piece.keyList:
            return None

        from_p = coords[0]
        for i in coords[1:3]:
            if len(i) > 1 or ord(i[0]) < 48 or ord(i[0]) > 52:
                return None
            else:
                coord_nums.append(int(i))
        to_p = tuple(coord_nums)
        return from_p, to_p

    def advanceWithPerson(self, line):
        """
        Advance the game with the command given by the player.
        :param line: player's move from command line
        """
        ret = self.parseMoveFromLine(line)
        opponent = Constants.MIN if self.player == Constants.MAX else\
            Constants.MAX
        if ret != None:
            from_p, to_p = ret[0], ret[1]
            if (self.player == Constants.MAX and\
                    self.board.pieceIdentity(from_p) == Piece.W) or\
                    (self.player == Constants.MIN and\
                    self.board.pieceIdentity(from_p) != Piece.W):
                return False

            nextMove = self.board.move(from_p, to_p)
            if nextMove != None:
                self.board = nextMove
                self.ply += 1
                self.player = opponent
                self.successors = self.board.successors(self.player)
                return True
        return False

def runGame(depth_limit, search):
    """
    Instantiates and runs a game.
    :param depth_limit: the depth limit of the search strategy used
    :param search: search strategy - minimax/alphabeta
    """
    game = Game(depth_limit)
    print("Wights or Dragons or all AI?")
    print(":: Options :: W for Wights, D for Dragons, AI for all AI")
    SELECT_PLAYER = False
    while not SELECT_PLAYER:
        line = input()
        if line == 'W':
            HUMAN = True
            ALL_AI = False
        elif line == 'D':
            HUMAN = False
            ALL_AI = False
        elif line == 'AI':
            HUMAN = False
            ALL_AI = True
        else:
            print("Please enter again...")
            continue
        break

    while not game.isAtEndGame():
        print("Current Board at ply: " + str(game.ply), "; Player:",
            game.player)
        print(game.board)
        if HUMAN and not ALL_AI:
            print("> Enter move: ", end='')
            while not game.advanceWithPerson(input()):
                print("!!Bad Move!! Please enter again...")
                print("> Enter move again: ", end='')
        else:
            game.advanceWithAI(search)
        HUMAN = not HUMAN
    print("Final State:")
    print(game.board)
    print(Constants.MIN if game.player == Constants.MAX else Constants.MAX,\
            "wins!")
