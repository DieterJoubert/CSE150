#!/usr/bin/python2
"""Contains routines for running the game."""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

import sys, os
from types import MethodType
from multiprocessing import Process, Queue
try:
    from queue import Empty
except ImportError:
    from Queue import Empty

from assignment2 import Player, State, Action


class Game(object):
    def __init__(self, M, N, K, player_classes, timeout=None):
        self.players = Player.create_players(player_classes)
        self.state = State.initial(M, N, K, self.players[0])
        self.timeout = timeout

    def play(self):
        while not self.state.is_terminal():
            self.before_move()
            next_move = self.request_move()
            self.state = self.state.result(next_move)
            self.after_move()

    def request_move(self):
        # state = copy.deepcopy(self.state)
        state = self.state
        player = self.state.to_play

        if self.timeout is None:
            # No timeout, just use a single process
            action = self.state.to_play.move(state)
        else:
            # For passing the messages back and forth
            self.result_q = Queue(1)
            self.signal_q = Queue(1)

            # Dynamically augment the player instance
            def is_time_up(self):
                try:
                    self._signal_q.get_nowait()
                    return True
                except Empty:
                    return False

            def do_move(self, state, result_q, signal_q):
                sys.stdin = os.fdopen(self.fileno)
                self._signal_q = signal_q
                result_q.put_nowait(self.move(state))

            player.is_time_up = MethodType(is_time_up, player)
            player.do_move = MethodType(do_move, player)
            player.fileno = sys.stdin.fileno()


            # Boot a process for the player move
            move_process = Process(target=player.do_move, args=(state, self.result_q, self.signal_q))
            move_process.start()

            action = None
            try:
                action = self.result_q.get(True, self.timeout)

            except Empty:
                # Send the "time is up" warning
                self.signal_q.put_nowait(0)

                # Wait one second and get the move
                try:
                    action = self.result_q.get(True, 1)
                except Empty:
                    pass

            # Clear queues
            try:
                self.signal_q.get_nowait()
            except Empty:
                pass

            try:
                self.result_q.get_nowait()
            except Empty:
                pass

            if move_process.is_alive():
                move_process.terminate()
                move_process.join(1)

            if action is None:
                # If a move wasn't placed on the result pipe in time, play a random move
                action = self.state.actions()[0]

        return action


class ConsoleGame(Game):
    def before_move(self):
        print(self.state)
        print('')

    def after_move(self):
        print(self.state.last_action)

    def play(self):
        super(ConsoleGame, self).play()

        print(self.state)

        if self.state.winner_color == 0:
            print("Draw!")
        else:
            winner = next((player for player in self.players if player.color == self.state.winner_color))
            print("%s won!" % str(winner))


if __name__ == '__main__':
    import sys
    import glob
    import os.path as op
    import inspect

    if len(sys.argv) < 5:
        print("%s: M N K timeout player1_class player2_class" % sys.argv[0])

    sys.argv.pop(0)
    M = int(sys.argv.pop(0))
    N = int(sys.argv.pop(0))
    K = int(sys.argv.pop(0))
    timeout = int(sys.argv.pop(0))
    if timeout == -1:
        timeout = None

    player_names = sys.argv

    # Load all player classes from *_player.py files
    # in the current directory and solutions directory
    player_files = glob.glob('*_player.py') + glob.glob('../solutions/*_player.py')
    for player_file in player_files:
        sys.path.append(op.abspath(op.dirname(player_file)))

    modules = [__import__(op.splitext(op.basename(f))[0]) for f in player_files]
    names = dict([(name, module) for module in modules for name in dir(module) if
                  inspect.isclass(getattr(module, name)) and issubclass(getattr(module, name), Player)])
    player_classes = [getattr(names[name], name) for name in player_names]

    game = ConsoleGame(M, N, K, player_classes, timeout)

    # Read state from console, if provided
    if not sys.stdin.isatty():
        input_string = sys.stdin.read().strip()
        if len(input_string) > 0:
            game.state = eval(input_string)
            game.state.to_play = game.players[game.state.last_action.color % len(game.players)]
        sys.stdin = open('/dev/tty')

    game.play()