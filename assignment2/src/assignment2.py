# -*- coding: utf-8 -*-
"""Contains the connect-m,n,k game state, player and actions classes.

These should not be modified!
"""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'


class Player(object):
    """The base class for all agents."""

    def __init__(self, color, next=None):
        self.color = color
        self.next = next

    @staticmethod
    def create_players(player_classes):
        """Instantiates Player objects from the given list of Player subclasses."""
        players = [player_class(i + 1) for i, player_class in enumerate(player_classes)]
        for i, player in enumerate(players):
            player.next = players[(i + 1) % len(players)]
        return players

    def __int__(self):
        return self.color

    def __hash__(self):
        return self.color

    def __eq__(self, other):
        return self.color == other.color

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.color)

    def __str__(self):
        return "%s (%d)" % (self.name, self.color)

    @property
    def name(self):
        return self.__class__.__name__

    def is_time_up(self):
        """Returns True when the time is up."""
        return False

    def move(self, state):
        """Calculates the best move from the given board.
        Each agent should implement this method.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """
        raise NotImplemented


class Action(object):
    """Represents a placement of stone of the color at a location."""

    def __init__(self, color, location):
        self.color = color
        self.location = location

    def __hash__(self):
        return hash((self.color, self.location))

    def __eq__(self, other):
        return self.color == other.color and self.location == other.location

    def __repr__(self):
        return "Action(%d, %s)" % (self.color, repr(self.location))

    def __str__(self):
        return "Player %d played at %s" % (self.color, str(self.location))


class State(object):
    """Represents the board state. The 'board' attribute represents the game board in an MxN tuple of tuples.
    In this array, 0 represents the empty location, and 1 and 2 represent the stones placed by players
    1 and 2, respectively (which are called 'colors').
    """

    @classmethod
    def initial(cls, M, N, K, to_play):
        """Creates the initial state.

        Args:
            M (int): vertical length of the board.
            N (int): horizontal length of the board.
            K (int): the number of stones that must be connected to win the game.
            first_player (Player): the first player who gets to play.
        """
        assert K <= min(M, N), "K (%d) must be less than the board size (%d x %d)" % (K, M, N)
        return cls(K, ((0,) * N,) * M, None, to_play)

    def __init__(self, K, board, last_action, to_play=None):
        """Internal 'copy' constructor.

        Args:
            K (int): the number of connected stones needed to win.
            board (tuple of tuple): current board state.
            last_action (Action): the last stone placement action that yielded this state.
        """
        self.K = K
        self.board = board
        self.last_action = last_action
        assert last_action is None or self.board[last_action.location[0]][last_action.location[1]] == last_action.color
        self.to_play = to_play
        self._is_terminal = None
        self._winner_color = None

    def __eq__(self, other):
        """Returns whether two State instances represent the same board state."""
        return self.board == other.board

    def __hash__(self):
        """Returns the hash representing the current board state."""
        return hash(self.board)

    def __str__(self):
        """Returns the string representation of the board."""
        return "%s (%d ply)" % \
               ('\n'.join([''.join([str(c) for c in row]) for row in self.board]), self.ply)

    @property
    def M(self):
        """Returns the vertical size of the board."""
        return len(self.board)

    @property
    def N(self):
        """Returns the horizontal size of the board."""
        return len(self.board[0])

    @property
    def ply(self):
        """Returns the number of moves (plys) taken to reach this state."""
        return sum([1 for row in self.board for cell in row if cell > 0])

    def is_full(self):
        """Returns whether there are no more moves available for the board."""
        return all(map(all, self.board))

    def is_terminal(self):
        """Returns whether this state is a terminal state (win for the player or a draw).
        """
        if self._is_terminal is None:
            if self.last_action is None:
                self._is_terminal = False

            # Win for the player who last played
            elif self.is_win():
                self._is_terminal = True
                self._winner_color = self.last_action.color

            # Draw
            elif self.is_full():
                self._is_terminal = True
                self._winner_color = 0

        return self._is_terminal

    @property
    def winner_color(self):
        """Returns the color of the player who won, or 0 if it was a draw,
        *only if it is a terminal state* (is_terminal() must have been True).
        """
        assert self._is_terminal, "is_terminal() must True to calculate the winner"
        return self._winner_color

    def utility(self, for_player):
        """Returns the utility for the given player *if it is a terminal state*
        (is_terminal() must have been True).
        """
        assert self._is_terminal, "is_terminal() must True to calculate the utility value"
        if self._winner_color == 0:
            return 0.0

        return 1.0 if self._winner_color == for_player.color else -1.0

    def is_win(self):
        """Calculates whether the last action resulted in this state being a win for that player."""
        li, lj = self.last_action.location
        assert 0 <= li < self.M and 0 <= lj < self.N, "%s is outside of the board" % self.last_action.location
        color = self.last_action.color

        # The coordinates where we want to start the checks
        t = max(li - self.K + 1, 0)
        b = min(self.M - self.K, li)
        l = max(lj - self.K + 1, 0)
        r = min(self.N - self.K, lj)

        # Check vertical
        for i in range(t, b + 1):
            if all((self.board[i + k][lj] == color for k in range(self.K))):
                return True

        # Check horizontal
        for j in range(l, r + 1):
            if all((self.board[li][j + k] == color for k in range(self.K))):
                return True


        # Check top left to bottom right diagonal
        for d in range(-min(li - t, lj - l), min(b - li, r - lj) + 1):
            if all((self.board[li + d + k][lj + d + k] == color for k in range(self.K))):
                return True


        # Check bottom left to top right diagonal
        for d in range(-min(self.M - 1 - li, lj, self.K - 1), min(li - self.K + 1, self.N - self.K - lj, 0) + 1):
            if all((self.board[li - d - k][lj + d + k] == color for k in range(self.K))):
                return True

        return False

    def actions(self):
        """Returns a list of available actions (where the board has value of 0).

        Returns:
            A list of actions that can be taken from the current state.
        """
        stone_color = self.to_play.color
        return [Action(stone_color, (i, j))
                for i, row in enumerate(self.board) for j, v in enumerate(row) if v == 0]

    def result(self, action):
        """Return the new state resulting from the given action.
        """
        li, lj = action.location
        assert self.board[li][lj] == 0, "Illegal action: %s" % repr(action)

        # Convert to list, modify and convert back to tuples
        board = list(map(list, self.board))
        board[li][lj] = action.color
        return State(self.K, tuple(map(tuple, board)), action, self.to_play.next)
