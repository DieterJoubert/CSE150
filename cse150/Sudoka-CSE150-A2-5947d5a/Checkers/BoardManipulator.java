package Checkers;

import java.util.Vector;

/**
 * This class generates all moves for its respective Board. It is intended to be accessed 
 * solely through the interface provided by the Game class.
 * @author mhtong
 *
 */
public class BoardManipulator {
	/**The Board being manipulated*/
	protected Board board;
	
	/**A growing vector of possible successor states*/
	protected Vector<Board> moves;
	
	/**True if a jump has been found as a possible action. When possible, jumps must be taken.*/
	protected boolean isJump;
	
	/**True if P1's turn, false if P2's turn.*/
	protected boolean p1Turn;
	
	/**The current effective # of moves, taken from the passed in board*/
	protected int depth;

	/**
	 * The constructor.
	 * @param b The Board to be manipulated.
	 */
	protected BoardManipulator(Board b){
		board = b;
		p1Turn = b.p1Turn;
		depth = b.depth;
		isJump = false;
	}

	/**
	 * Finds the successor Board states of the board being manipulated.
	 * @return A Vector of Boards corresponding to all Board states reachable by valid actions from the Board being manipulated
	 */
	protected Vector<Board> expand(){	
		moves = new Vector <Board> ();

		for (int i = 0; i<8; i++){
			for (int j = 0; j<8; j++){
				if ((p1Turn && (board.board[i][j] > 0)) ||
						((!p1Turn && (board.board[i][j] == -2)))){
					jumpPiece(i,j,1,1);
					jumpPiece(i,j,-1,1);
					if (!isJump)
						movePiece(i,j,1);
				}
				if ((!p1Turn && (board.board[i][j] < 0)) ||
						((p1Turn && (board.board[i][j] == 2)))){
					jumpPiece(i,j,1,-1);
					jumpPiece(i,j,-1,-1);
					if (!isJump)
						movePiece(i,j,-1);
				}				
			}
		}
		return moves;
	}

	/**
	 * Attempts to move the piece at (i,j) to (i +/- 1, j+d). If successful, added to moves.
	 * @param i The y coord of the piece
	 * @param j The x coord of the piece
	 * @param d The direction of movement
	 */
	private void movePiece(int i, int j, int d){
		Board nb = board.move(i, j, -1, d);
		if (nb != null){
			addMove(nb);
		}

		nb = board.move(i, j, 1, d);
		if (nb != null){
			addMove(nb);
		}
	}

	/**
	 * Attempts to jump the piece at (i+lr, j+d) using the piece at (i,j).
	 * @param i The y coord of the jumping piece
	 * @param j The x coord of the jumping piece
	 * @param lr Jump to left(-1) or right (1)?
	 * @param d Direction of jump, forward or back?
	 */
	private void jumpPiece(int i, int j, int lr, int d){
		jumpPiece(i, j, lr, d, board);
	}
	
	/**
	 * Attempts to jump the piece at (i+lr, j+d) using the piece at (i,j) on board b. If successful, it recursively attempts to keep jumping. All valid jump sequences are added to moves. If it is the first jump found, moves is cleared to force the jump.
	 * @param i The y coord of the jumping piece
	 * @param j The x coord of the jumping piece
	 * @param lr Jump to left(-1) or right (1)?
	 * @param d Direction of jump, forward or back?
	 * @param b The board to check
	 * @return True if jump occurs, false else.
	 */
	private boolean jumpPiece(int i, int j, int lr, int d, Board b){
		Board nb  = b.jump(i, j, lr, d);
		boolean moreJumps = false;
		i=i+2*lr;
		j=j+2*d;
		
		if (nb != null){
			if ((p1Turn && (nb.board[i][j] > 0)) ||
					((!p1Turn && (nb.board[i][j] == -2)))){
				moreJumps = jumpPiece(i,j,1,1,nb) || moreJumps;
				moreJumps = jumpPiece(i,j,-1,1,nb) || moreJumps;
			}
			if ((!p1Turn && (nb.board[i][j] < 0)) ||
					((p1Turn && (nb.board[i][j] == 2)))){
				moreJumps = jumpPiece(i,j,1,-1,nb) || moreJumps;
				moreJumps = jumpPiece(i,j,-1,-1,nb) || moreJumps;
			}
			if (!moreJumps){
				if (!isJump){
					moves = new Vector<Board>();
					isJump = true;
				}
				addMove(nb);
			}
			return true;
		}
		else{
			return false;
		}
	}
	
	/**
	 * This adds a Board state to the list of moves and sets the relevant fields in the new Board.
	 * @param b
	 */
	private void addMove(Board b){
		b.depth = depth + 1;
		b.p1Turn = !p1Turn;
		moves.add(b);
	}
}
