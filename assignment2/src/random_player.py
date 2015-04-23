# -*- coding: utf-8 -*-
__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

import random

from assignment2 import Player


class RandomPlayer(Player):
    def move(self, state):
        """Plays a random legal move.

        Args:
            state (State): The current state of the board.

        Returns:
            the next random move (Action)
        """

        actions = state.actions()
        return actions[random.randrange(len(actions))]
