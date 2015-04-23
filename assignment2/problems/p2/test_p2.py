"""Test case runner for Sharif Judge.

For each input in in/input*.txt, Sharif Judge will invoke this file as:

    python test_p1.py submitted_file.py <$inputfile >out

and the output file is later diff'ed against out/output*.txt file.
"""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

import os
import sys
import inspect

from assignment2 import Player, State, Action


def run_code_from(python_file, input_text):
    # Load the player class from the specified .py file
    sys.path.append(os.path.abspath(os.path.dirname(python_file)))
    module = __import__(os.path.splitext(os.path.basename(python_file))[0])
    player_class = next(getattr(module, name) for name in dir(module) if
                        inspect.isclass(getattr(module, name)) and issubclass(getattr(module, name), Player))
    players = Player.create_players([player_class, Player])  # Second player is a dummy
    state = eval(input_text)
    state.to_play = players[0]
    return repr(players[0].move(state))


if __name__ == '__main__':
    print(run_code_from(sys.argv[1], sys.stdin.read().strip()))