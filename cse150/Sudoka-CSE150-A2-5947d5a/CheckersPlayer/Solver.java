package CheckersPlayer;

import Checkers.Board;

/**
 * All student's move suggesting classes must implement this interface. It ensure that their class can return an action.
 * @author mhtong
 * @author baduncan
 *
 */
public interface Solver {
	/**
	 * Given a board, this returns the index to the move to be taken. The index is into the Vector of Boards returned by expand.
	 * @param b The current game board
	 * @return The move to be taken.
	 */
	int selectMove(Board b);
}
