# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

from assignment2 import Player, State, Action

INFINITY = 1000
NEG_INFINITY = -1000
trans_table = {}

class AlphaBetaPlayer(Player):
    def move(self, state):
        """Calculates the best move from the given board using the minimax algorithm with alpha-beta pruning.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # TODO implement this
        return self.alpha_beta_search(state)

    def alpha_beta_search(self, state):
        #get results of all possible moves from initial state, find max, return move
        trans_table = {}
        results = [self.min_value(state.result(a), NEG_INFINITY, INFINITY) for a in state.actions()]
        index = results.index(max(results))
        return state.actions()[index]

    def min_value(self, state, alpha, beta):
        h = hash(state)

        #lookup if value is already in transposition table
        if trans_table.has_key(h):
            return trans_table[h]

        if state.is_terminal():
            trans_table[h] = state.utility(self)
            return state.utility(self) 

        v = INFINITY

        for a in state.actions():
            v = min(v, self.max_value(state.result(a), alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                trans_table[h] = v
                return v

        trans_table[h] = v
        return v

    def max_value(self, state, alpha, beta):
        h = hash(state)
        
        #lookup if value is already in transposition table
        if trans_table.has_key(h):
            return trans_table[h]

        if state.is_terminal():
            trans_table[h] = state.utility(self)
            return state.utility(self)

        v = NEG_INFINITY

        for a in state.actions():
            v = max(v, self.min_value(state.result(a), alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                trans_table[h] = v
                return v

        trans_table[h] = v
        return v
