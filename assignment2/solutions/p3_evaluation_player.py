# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

import heapq

from assignment2 import Player

test1 =  [[0,2,1,0],[0,1,2,0],[0,0,0,0],[0,0,0,0]]
test2 = [[0,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,1,0,1,0],[0,1,0,0,1,0],[0,0,0,0,1,0],[0,0,0,0,2,0]]
test3 = [[0,1,0,0,0],[1,0,1,0,0],[0,0,0,1,0]]
test4 = [[1,0,0,0],[0,1,0,1],[1,0,1,0],[0,1,0,0],[1,0,1,0],[0,0,0,1],[0,0,0,0]]


class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-ply look-ahead with a simple evaluation function.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # *You do not need to modify this method.*
        best_move = None
        max_value = -1.0
        my_color = state.to_play.color

        for action in state.actions():
            if self.is_time_up():
                break

            result_state = state.result(action)
            value = self.evaluate(result_state, my_color)
            if value > max_value:
                max_value = value
                best_move = action

        # Return the move with the highest evaluation value
        return best_move

    def evaluate(self, state, color):
        """Evaluates the state for the player with the given stone color.

        This function calculates the length of the longest ``streak'' on the board
        (of the given stone color) divided by K.  Since the longest streak you can
        achieve is K, the value returned will be in range [1 / state.K, 1.0].

        Args:
            state (State): The state instance for the current board.
            color (int): The color of the stone for which to calculate the streaks.

        Returns:
            the evaluation value (float), from 1.0 / state.K (worst) to 1.0 (win).
        """

        # TODO implement this

        ### Comment out for direct testing ###
        board = state.board
        height = state.M
        width = state.N
        #######################################

        ### For direct testing ###
        #board = state
        #width = len(board[0])
        #height = len(board)
        ###########################

        val = 0

        #horizontal
        for row in range(height):
            temp = 0
            for col in range(width):
                if board[row][col] == color:
                    temp += 1 
                else:
                    val = max(temp, val)
                    temp = 0

            val = max(temp, val)

        #vertical
        for col in range(width):
            temp = 0
            for row in range(height):
                if board[row][col] == color:
                    temp += 1
                else:
                    val = max(temp, val)
                    temp = 0
                    
            val = max(temp, val)


        #diagonals running top left to bottom right, starting at horizontal top
        for col in range(0,width):
            temp = 0
            x = col
            y = 0
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    temp = temp + 1 
                else:
                    val = max(temp, val)
                    temp = 0
                x += 1
                y += 1
            val = max(temp, val)

        #diagonals running top left to bottom right, starting at vertical left
        for row in range(0,height):
            temp = 0
            x = 0
            y = row
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    temp = temp + 1 
                else:
                    val = max(temp, val)
                    temp = 0
                x += 1
                y += 1
            val = max(temp, val)


        #diagonals running top right to bottom left, start at horizontal top
        for col in range(0,width):
            temp = 0
            x = col
            y = 0
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    temp = temp + 1 
                else:
                    val = max(temp, val)
                    temp = 0
                x -= 1
                y += 1
            val = max(temp, val)

        #diagonals running top right to bottom left, starting at vertical right
        for row in range(0,height):
            temp = 0
            x = width-1
            y = row
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    temp = temp + 1 
                else:
                    val = max(temp, val)
                    temp = 0
                x -= 1
                y += 1
            val = max(temp, val)

        return float(val) / float(state.K)




### For Direct Testing ###
#player1 = EvaluationPlayer(1)

#print player1.evaluate(test1, 1)
#print player1.evaluate(test2, 1)
#player1.evaluate(test3, 1)
#player1.evaluate(test4, 1)
##############################
