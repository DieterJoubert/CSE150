# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

from assignment2 import Player, State, Action

from random import shuffle

INFINITY = 1000         
NEG_INFINITY = -1000


class YourCustomPlayer(Player):

    trans_table = {}
    MAX_DEPTH = 0

    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'Dank_Heuristix'

    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.

        Returns:
            your next Action instance
        """


        my_move = state.actions()[0]
        last_move = my_move


        ### *********** TIMING CONTROL AND ITERATIVE DEEPENING **********

        while not self.is_time_up():
            
            #print "Depth: " + str(self.MAX_DEPTH)
            my_move,utility = self.do_the_magic(state, self.MAX_DEPTH)

            if my_move is None:
                ########### Hardcoded first move near center ###########
                if state.ply < 2 and state.M > 3 and state.N > 3:
                    if state.M % 2 == 0:
                        self.MAX_DEPTH -= 1
                        return state.actions()[int(state.M*state.N/2) + int(state.N/2)]
                    self.MAX_DEPTH -= 1
                    return state.actions()[int(state.M*state.N/2)]
                ########################################################
                self.MAX_DEPTH -= 1
                #print "quit correctly"
                return last_move

            if utility == INFINITY:
                self.MAX_DEPTH -= 1
                return my_move

            last_move = my_move
            self.MAX_DEPTH += 1

            # trans_table needs to be reset after every complete search 
            # otherwise the states will not be evaluated deeper
            self.trans_table = {}



        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        self.MAX_DEPTH -= 1
        return my_move

    def do_the_magic(self, state, DEPTH):
        # Do the magic, return the first available move!

        ### Implement some move ordering at this point ###

        results = ([0] * len(state.actions()))
        order = range(len(state.actions()))
        shuffle(order)

        # This is random move ordering, utility ordering may be better?
        for i in order:
            results[i] = self.min_value(state.result(state.actions()[i]), NEG_INFINITY, INFINITY, DEPTH)
            if results[i] is None:
                    return None, None
        #print "Max Utility: " + str(max(results))
        ##################################################

        self.trans_table = {}

        #results = [self.min_value(state.result(a), NEG_INFINITY, INFINITY, MAX_DEPTH) for a in state.actions()]
        if max(results) == NEG_INFINITY:
            for i in order:
                results[i] = self.min_value(state.result(state.actions()[i]), NEG_INFINITY, INFINITY, 0)
                if results[i] is None:
                    return None, None

        index = results.index(max(results))
        #print max(results)

        return state.actions()[index], max(results)

    def min_value(self, state, alpha, beta, depth):
        h = hash(state)

        #lookup if value is already in transposition table
        if self.trans_table.has_key(h):
            return self.trans_table[h]

        if state.is_terminal():
            v = INFINITY * state.utility(self)
            self.trans_table[h] = v
            return v

        if self.is_time_up():
            return None

        if depth == 0:
            #self.Count += 1
            v = self.evaluate(state)
            self.trans_table[h] = v
            return v

        v = INFINITY

        for a in state.actions():
            temp = self.max_value(state.result(a), alpha, beta, depth - 1)
            if temp is None:
                return None
            v = min(v, temp)
            beta = min(beta, v)
            if beta <= alpha:
                self.trans_table[h] = v
                return v

        self.trans_table[h] = v
        return v

    def max_value(self, state, alpha, beta, depth):
        h = hash(state)
        
        #lookup if value is already in transposition table
        if self.trans_table.has_key(h):
            return self.trans_table[h]

        if state.is_terminal():
            v = INFINITY * state.utility(self)
            self.trans_table[h] = v
            return v

        if self.is_time_up():
            return None

        if depth == 0:
            #self.Count += 1
            v = self.evaluate(state, True)
            self.trans_table[h] = v
            return v

        v = NEG_INFINITY

        for a in state.actions():
            temp = self.min_value(state.result(a), alpha, beta, depth - 1)
            if temp is None:
                return None
            v = max(v, temp)
            alpha = max(alpha, v)
            if alpha >= beta:
                self.trans_table[h] = v
                return v

        self.trans_table[h] = v
        return v


    ### Heuristic Implementation Should Be Here ###

    def evaluate(self, state, flag = False):
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
        color = state.to_play.color

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

        #val = [0,0,0,0]
        #val2 = [0,0,0,0]

        # Potentials hold maximum utility found
        potential1 = 0
        potential2 = 0

        ############# Variable Definitions #####################

        # streak1 = length of streak for self
        # space1 = self streak + open space
        # total1 = total of own stones in valid row
        # maxStreak1 = highest streak in current (unborken) line

        # streak2 = length of streak for opponent
        # space2 = opponent streak + open space
        # total2 = total of opponent stones in current (unbroken) line
        # maxStreak2 = highest streak in current (unborken) line
        ########################################################

        ### Algorithm ###
        # We check all horizontals, verticals, and diagonals for maximum
        # utility of the move. Utility is a factor of the longest streak
        # in the line, how many of a players stones (total) are in the line
        # and how much space (which includes blanks and player's stones) is
        # in the line. The maximum utility is computed for both the player
        # and the opponent in this manner and the actual utility returned is
        # the difference between them. Wins and losses evaluate to "infinity"
        # and negative "infinity" respectively.

        ### ************************************
        #   Utility computation is exactly the same for all directions
        #   The computational bodies are the same, only the array checking
        #   is different
        ### ************************************

        #horizontal
        for row in range(height):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            for col in range(width):

                # If we hit our own color
                # (Opponents line is now broken)
                if board[row][col] == color:

                    # If space < K, the streak is useless
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                # Else if we hit an empty space    
                elif board[row][col] == 0:

                    # record current streaks in case we run into our
                    # own pieces again (unbroken line)
                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                # Else we hit an opponent's piece (Our line is now broken)    
                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0

            # Got to the end of the line, set potentials as usual
            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)

        #vertical
        for col in range(width):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            for row in range(height):

                # If we hit our own color
                # (Opponents line is now broken)
                if board[row][col] == color:
                    # If space < K, the streak is useless
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                # Else if we hit an empty space
                elif board[row][col] == 0:

                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                # Else we hit an opponent's piece (Our line is now broken)
                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0

            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)


        #diagonals running top left to bottom right, starting at horizontal top
        for col in range(0,width):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            x = col
            y = 0
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                elif board[y][x] == 0:
                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0
                x += 1
                y += 1
            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)

        #diagonals running top left to bottom right, starting at vertical left
        for row in range(0,height):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            x = 0
            y = row
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                elif board[y][x] == 0:
                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0
                x += 1
                y += 1
            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)


        #diagonals running top right to bottom left, start at horizontal top
        for col in range(0,width):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            x = col
            y = 0
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                elif board[y][x] == 0:
                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0
                x -= 1
                y += 1
            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)

        #diagonals running top right to bottom left, starting at vertical right
        for row in range(0,height):
            streak1 = 0
            space1 = 0
            streak2 = 0
            space2 = 0
            total1 = 0
            total2 = 0
            maxStreak1 = 0
            maxStreak2 = 0
            x = width-1
            y = row
            while( 0 <= x < width and 0 <= y < height ):
                if board[y][x] == color:
                    if space2 >= state.K:
                        #val2[0] = max(streak2, val2[0])
                        maxStreak2 = max(maxStreak2, streak2)
                        potential2 = max(potential2, 3*maxStreak2 + 2*total2)
                    streak1 += 1
                    space1 += 1
                    total1 += 1
                    maxStreak2 = 0
                    streak2 = 0
                    space2 = 0
                    total2 = 0

                elif board[y][x] == 0:
                    maxStreak1 = max(maxStreak1, streak1)
                    maxStreak2 = max(maxStreak2, streak2)
                    space1 += 1
                    space2 += 1
                    streak1 = 0
                    streak2 = 0

                else:
                    if space1 >= state.K:
                        #val[0] = max(streak1, val[0])
                        maxStreak1 = max(maxStreak1, streak1)
                        potential1 = max(potential1, 3*maxStreak1 + 2*total1)
                    streak2 += 1
                    space2 += 1
                    total2 += 1
                    maxStreak1 = 0
                    streak1 = 0
                    space1 = 0
                    total1 = 0
                x -= 1
                y += 1
            if space1 >= state.K:
                maxStreak1 = max(maxStreak1, streak1)
                potential1 = max(potential1, 3*maxStreak1 + 2*total1)
            if space2 >= state.K:
                maxStreak2 = max(maxStreak2, streak2)
                potential2 = max(potential2, 3*maxStreak2 + 2*total2)

        # If our code detects a forced loss by an "optimal" player
        # the search will be redone with a depth of one and the move
        # returned will be that which minimizes the opponent's utility
        # in the hopes that a non-optimal player makes a miss step
        if flag:
            return potential1 - potential2
        return potential2 - potential1

