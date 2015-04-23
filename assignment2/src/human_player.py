# -*- coding: utf-8 -*-
__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

from assignment2 import Player


class HumanPlayer(Player):
    def move(self, state):
        """Reads the next move from the console.
        The move should be entered as two numbers separated by a space, like '3 3'.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """
        action = None
        while not self.is_time_up() and action is None:
            input_location = tuple([int(n) for n in raw_input('%s move?' % str(self)).strip().split(' ')])
            action = next((action for action in state.actions() if action.location == input_location), None)
            if action is None:
                print "Invalid input. Enter two numbers separated by a space!"

        return action
