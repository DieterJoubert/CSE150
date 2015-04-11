package Checkers;

/**
 * This represents a game state. It contains a current checkerboard with all pieces 
 * marked, a note on whose turn it is, and a counter of how many moves have been 
 * played. It also provides action primitives for moves and jumps, but these are 
 * for board manipulation only and are not to be used by Solver classes.
 * @author mhtong
 *
 */
public class Board {

	/**
	 * The board itself. Key:
	 * 0 - Empty space
	 * 1 - P1 piece
	 * 2 - P1 king
	 * -1 - P2 piece
	 * -2 - P2 king
	 */
	public int board[][];
	
	/**
	 * The dimensions of the square board.
	 */
	public static final int BOARDSIZE = 8;
	
	/**How many rows to fill with pieces at initialization*/
	public static final int STARTROWS = 3;
	
	/**True if P1's turn, false if P2's*/
	public boolean p1Turn;
	
	/**The number of moves to reach this state*/
	protected int depth;

	/**
	 * The default consructor. Creates a initialized board.
	 */
	public Board(){
		board = new int[BOARDSIZE][BOARDSIZE];
		reset();
		p1Turn = true;
		depth = 0;
	}

	/**
	 * Creates a Board with the specified board. Other fields must be set prior to access.
	 * @param nb The board
	 */
	public Board(int nb[][]){
		board = new int[BOARDSIZE][BOARDSIZE];
		for (int i = 0; i < BOARDSIZE; i++)
			for (int j = 0; j < BOARDSIZE; j++)
				board[i][j] = nb[i][j];
	}
	
	/**
	 * Creates a copy of the passed in board
	 */
	public Board(Board b){
		this(b.board);
		depth = b.depth;
		p1Turn = b.p1Turn;
	}

	/**
	 * Resets the board to the initial state.
	 *
	 */
	protected void reset(){
		int counter = 0;
		for (int i = 0; i < BOARDSIZE; i++){
			int j = 0;
			for (j = 0; j < STARTROWS; j++){
				if (counter % 2 == 0){
					board[i][j] = 1;
				}
				else{
					board[i][j] = 0;
				}
				counter++;
			}
			for (j = BOARDSIZE-STARTROWS; j < BOARDSIZE; j++){
				if (counter % 2 == 0){
					board[i][j] = -1;
				}
				else{
					board[i][j] = 0;
				}
				counter++;
			}
			counter++;
		}
	}

	/**
	 * Tries to move the piece at (i,j) to (i+iInc, j+jInc).
	 * @param i The y coord of the piece
	 * @param j The x coord of the piece
	 * @param iInc The y increment of the move (+/- 1)
	 * @param jInc The y increment of the move (+/- 1)
	 * @return The new board state if move occurred, null else.
	 */
	protected Board move(int i, int j, int iInc, int jInc){
		if ((i+iInc < 0) || 
				(i+iInc >= BOARDSIZE) || 
				(j+jInc < 0) || 
				(j+jInc >= BOARDSIZE) || 
				(board[i][j]==0) || 
				(board[i+iInc][j+jInc]!=0) || 
				(iInc > 1) || 
				(jInc > 1))
			return null;
		Board nb = new Board(board);
		nb.board[i+iInc][j+jInc] = nb.board[i][j];
		nb.board[i][j] = 0;
		if ((nb.board[i+iInc][j+jInc] == 1) && (j+jInc == BOARDSIZE -1))
			nb.board[i+iInc][j+jInc] = 2;
		if ((nb.board[i+iInc][j+jInc] == -1) && (j+jInc == 0))
			nb.board[i+iInc][j+jInc] = -2;
		return nb;
	}

	/**
	 * Tries to jump the piece at (i+iInc,j+jInc) using the piece at (i, j).
	 * @param i The y coord of the piece
	 * @param j The x coord of the piece
	 * @param iInc The y increment of the move (+/- 1)
	 * @param jInc The y increment of the move (+/- 1)
	 * @return The new board state if jump occurred, null else.
	 */
	protected Board jump(int i, int j, int iInc, int jInc){
		int i2 = iInc*2;
		int j2 = jInc*2;
		if ((i+i2 < 0) || 
				(i+i2 >= BOARDSIZE) || 
				(j+j2 < 0) || 
				(j+j2 >= BOARDSIZE) || 
				(board[i][j]==0) || 
				(board[i+i2][j+j2]!=0) ||
				((board[i][j] < 0) && (board[i+iInc][j+jInc] <= 0)) ||
				((board[i][j] > 0) && (board[i+iInc][j+jInc] >= 0)) ||
				(iInc > 1) || 
				(jInc > 1))
			return null;
		Board nb = new Board(board);
		nb.board[i+i2][j+j2] = nb.board[i][j];
		nb.board[i+iInc][j+jInc] = 0;
		nb.board[i][j] = 0;
		if ((nb.board[i+i2][j+j2] == 1) && (j+j2 == BOARDSIZE -1))
			nb.board[i+i2][j+j2] = 2;
		if ((nb.board[i+i2][j+j2] == -1) && (j+j2 == 0))
			nb.board[i+i2][j+j2] = -2;
		return nb;
	}

	/**
	 * Gets the number of moves used to reach this state.
	 * @return number of moves used to reach this state.
	 */
	public int getDepth(){
		return depth;
	}

	/**
	 * This prints the board using red and black pieces Key:
	 * r: p1 piece
	 * R: p1 king
	 * b: p2 piece
	 * B: p2 king
	 *
	 */
	public void printBoard(){
		char c = ' ';
		for (int i = 0; i < BOARDSIZE; i++){
			for (int j = 0; j < BOARDSIZE; j++){
				switch(board[i][j]){
				case -2:
					c = 'B';
					break;
				case -1:
					c = 'b';
					break;
				case 0:
					c = ' ';
					break;
				case 1:
					c = 'r';
					break;
				case 2:
					c = 'R';
					break;
				}
				System.out.print(c + " ");
			}
			System.out.print("\n");
		}
		System.out.print("\n\n");
	}
	
	/**
	 * Sees whether all of p2's pieces have been eliminated.
	 * @return true if no pieces of p2 remain, false else
	 */
	public boolean p1win(){
		for (int i = 0; i < BOARDSIZE; i++)
			for (int j = 0; j < BOARDSIZE; j++)
				if (board[i][j] < 0)
					return false;
		return true;
	}
	
	/**
	 * Sees whether all of p1's pieces have been eliminated.
	 * @return true if no pieces of p1 remain, false else
	 */
	public boolean p2win(){
		for (int i = 0; i < BOARDSIZE; i++)
			for (int j = 0; j < BOARDSIZE; j++)
				if (board[i][j] > 0)
					return false;
		return true;
	}
}
