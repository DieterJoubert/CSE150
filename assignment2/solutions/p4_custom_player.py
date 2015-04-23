# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action


class YourCustomPlayer(Player):
    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'HAL9000'

    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.

        Returns:
            your next Action instance
        """
        my_move = state.actions()[0]

        while not self.is_time_up() and self.feel_like_thinking():
            # Do some thinking here
            my_move = self.do_the_magic(state)

        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        return my_move

    def feel_like_thinking(self):
        # You can code here how long you want to think perhaps.
        return False

    def do_the_magic(self, state):
        # Do the magic, return the first available move!
        return state.actions()[0]

