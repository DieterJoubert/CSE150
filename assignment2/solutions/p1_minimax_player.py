# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action

INFINITY = 1000
NEG_INFINITY = -1000

class MinimaxPlayer(Player):
    def move(self, state):
        """Calculates the best move from the given board using the minimax algorithm.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # TODO implement this
        return self.minimax_decision(state)

    def minimax_decision(self, state):
        results = [self.min_value(state.result(a)) for a in state.actions()]
        index = results.index(max(results))
        return state.actions()[index]

    def min_value(self, state):
        if state.is_terminal():
            return state.utility(self) 

        v = INFINITY
        actions = state.actions()

        for a in actions:
            v = min(v, self.max_value(state.result(a)))
        return v

    def max_value(self, state):
        if state.is_terminal():
            return state.utility(self)
        v = NEG_INFINITY
        actions = state.actions()

        for a in actions:
            v = max(v, self.min_value(state.result(a)))

        return v