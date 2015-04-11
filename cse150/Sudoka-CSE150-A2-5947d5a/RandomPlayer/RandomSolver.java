package RandomPlayer;

import CheckersPlayer.*;
import Checkers.Board;
import Checkers.Game;

/**
 * This class selects a move at random. It is included partly as a template and partly as another possible source of comparison.
 * @author mhtong
 * @author baduncan
 *
 */
public class RandomSolver implements Solver {
	public int selectMove(Board b) {
		int numMoves = Game.expand(b).size();
		if (numMoves == 0)
			return -1;
		return (int)Math.floor(Math.random() * numMoves);
	}
}
