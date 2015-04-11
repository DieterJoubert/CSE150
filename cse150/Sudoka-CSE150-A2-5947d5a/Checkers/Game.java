package Checkers;
import java.util.Vector;

/**
 * The Game class provides an interface for keeping track of a game, executing moves, and
 * generating valid successor states for any board in a way that respects the set limit.
 * Limits can either be set on the depth of expansion or on the total number of nodes being
 * expanded and are set up when the game is constructed. Many methods are static and are
 * used to provide key information during search. Solver's will not have access to the actual
 * instance of the Game.
 * @author mhtong
 *
 */
public class Game{
	/**The maximum number of expansions per move. No limit if 0.*/
	private static int lookLimit;
	
	/**The maximum depth of expansion per move. No limit if 0.*/
	private static int depthLimit;
	
	/**A counter of the number of expansions this move. Reset after each move.*/
	private static int lookCounter;
	
	/**True if playing with a limit on # of expansions per move, false otherwise.*/
	private static boolean counterPlay;
	
	/**True if playing with a limit on depth of search, false otherwise.*/
	private static boolean depthPlay;
	
	/**Depth is the number of moves played so far.*/
	private static int depth;
	
	/**The list of successor states reachable with valid moves. Indexes into this correspond with action numbers.*/
	private static Vector<Board> moves;
	
	/**The current Board of the Game.*/
	private static Board board;
	
	/**True if p1's turn, false if p2's turn.*/
	private static boolean p1Turn;
	
	/**
	 * Default constructor for the Game class. It triggers a search mode that is bounded by the depth of the search.
	 *
	 */
	public Game(){
		this(3,0);
	}
	
	

	/**
	 * The more specified constructor for the Game class. Search can be limited by depth and/or the total number of board states expanded. Providing a limit of 0 or less denotes no limit of that type.
	 * @param depthLim The max depth of search (0 for no limit)
	 * @param lookLim The max number of board states that can be expanded (0 for no limit)
	 */
	public Game(int depthLim, int lookLim){
		board = new Board();
		BoardManipulator bman = new BoardManipulator(board);
		moves = bman.expand();
		depthLimit = depthLim;
		lookLimit = lookLim;
		if (lookLim > 0)
			counterPlay = true;
		else
			counterPlay = false;
		if (depthLim > 0)
			depthPlay = true;
		else
			depthPlay = false;
		lookCounter = 0;
		depth = 0;
		p1Turn = true;
	}
	
	/**
	 * This accesses the current board of the game in progress.
	 * @return Current board of game
	 */
	public static Board getBoard(){
		return new Board(board);
	}

	/**
	 * This returns the successor states of the current board via all possible moves. Moves are indexed using this Vector.
	 * @return A Vector of Board states representing the results of all possible moves.
	 */
	public Vector<Board> expand(){
		return moves;
	}
	
	/**
	 * This returns the number of currently valid moves. A game ends when one player has no possible moves (usually because they are out of pieces).
	 * @return Number of valid moves for the current player.
	 */
	public static int getNumMoves(){
		return moves.size();
	}

	/**
	 * This expands the supplied board, providing all possible successor states to that board through any valid action. If playing with a depth limit or a expansion limit, will return null if a limit has been exceeded.
	 * @param b The board to be expanded. 
	 * @return A Vector of Board states representing the results of all possible moves, or null if a limit has been exceeded.
	 */
	public static Vector<Board> expand(Board b){
		if (counterPlay && (lookCounter >= lookLimit))
			return null;
		if (depthPlay && (b.depth - depth >= depthLimit))
			return null;
		lookCounter++;
		BoardManipulator bm = new BoardManipulator(b);
		return bm.expand();
	}


	/**
	 * This prints the current board.
	 *
	 */
	public static void printGame(){
		board.printBoard();
	}

	/**
	 * This exectutes the move denoted by a. a is an index into the Vector of Boards returned by expand(). THIS IS NOT TO BE CALLED BY STUDENT'S CODE.
	 * @param a An index into the Vector of Boards returned by expand(), signifying the action to be taken.
	 */
	public void doMove(int a){
		if (moves == null)
			throw new RuntimeException("Must expand current board before moving");
		if ((a<0) || (a>= moves.size()))
			throw new RuntimeException("Attempt to execute a non-existing action.");
		board = moves.elementAt(a);
		lookCounter = 0;
		depth++;
		p1Turn = board.p1Turn;
		BoardManipulator bm = new BoardManipulator(board);
		moves = bm.expand();
	}

	/**
	 * This returns the number of looks (expansions) left. -1 if there is no limit
	 * @return The number of expansions left, -1 if no limit.
	 */
	public static int getLooksLeft(){
		if (lookLimit == 0)
			return -1;
		return lookLimit - lookCounter;
	}
	
	/**
	 * Checks whether any of p2's pieces remain, signifying a win by p1
	 * @return true if p2 has no pieces, false else
	 */
	public boolean p1Win(){
		return board.p1win();
	}
	
	/**
	 * Checks whether any of 12's pieces remain, signifying a win by p2
	 * @return true if p1 has no pieces, false else
	 */
	public boolean p2Win(){
		return board.p2win();
	}
	
	/**
	 * This returns a Vector of Coords listing the board coordinates of all pieces 
	 * that can be captured the next turn. Technically this calls "expand", but 
	 * this call does not count against the total expansion count. If a piece can 
	 * be taken in multiple ways, it is repeated (the Coord class includes an 
	 * "equals" operator to aid in disambiguation - originally, it was going to be 
	 * returned as a Set, but a Vector has some additionaly info). Information
	 * about when a piece is taken in the case of multiple jumps is also 
	 * provided - namely, the jumpCount in the Coord is the count on the number of
	 * jumps prior to this being taken (0 for singleton jumps or the first jump in
	 * a multi-jump, 1 for the second jump in a multijump, etc).
	 * @param b The board to be analyzed
	 * @return A Vector of Coords of pieces that could be taken next turn
	 */
	public static Vector <Coord> getThreats(Board b){
		BoardManipulator bm = new BoardManipulator(b);
		Vector <Board> s = bm.expand();
		Vector <Coord> set = new Vector<Coord>();
		int jumpCount;
		for (Board c:s){
			jumpCount = 0;
			for (int i = 0; i < Board.BOARDSIZE; i++){
				for (int j = 0; j < Board.BOARDSIZE; j++){
					if ((p1Turn &&(b.board[i][j] < 0) && (c.board[i][j] == 0))||
							(!p1Turn && (b.board[i][j] > 0) && (c.board[i][j] == 0))){
						set.add(new Coord(i,j, jumpCount));
						jumpCount++;
					}
				}
			}
		}
		if (bm.isJump)
			return set;
		return null;
	}
}