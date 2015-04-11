import CheckersPlayer.Solver;
import Checkers.Game;
import Checkers.Board;
import Checkers.Coord;
import java.util.Vector;


/**
 * The player class provides a simple mechanism for having two Checker Solvers compete. Modify main to determine which two methods should be used.
 * @author mhtong
 * @author baduncan
 *
 */
public class Player {
	
	/**
	 * Runs two methods against each other.
	 * @param args Takes no arguments
	 */
	public static void main(String args[]){
    // TODO - replace these lines with your own solvers, as explained below
		Solver p1 = new RandomPlayer.RandomSolver();
		Solver p2 = new RandomPlayer.RandomSolver();
    // TODO - Replace "TeamName" in the below lines of code with your actual
    // team name. You will also have to rename the "TeamName" folder to this
    // same name. After these changes the below lines need to compile as shown
    // (Class names must match and constructor must not take arguments)
    // This is how I will create your Players for grading.
    //
    // Solver p1 = new TeamName.MinimaxSolver();
    //
    // Solver p2 = new TeamName.AlphaBetaSolver();
    // OR
    // Solver p2 = new TeamName.CustomSolver();
    //
    // etc...
    //
    // The only provided files you should change are "TeamName"/*Solver.java
    // and this file, and in this file you should only make changes where
    // indicated by "TODO"

		play(p1,p2);
	}
	
	/**
	 * Competes the two Solver's against each other
	 * @param p1 P1's Solver
	 * @param p2 P2's Solver
	 */
	public static void play(Solver p1, Solver p2){
		int a;
		Board b;
    // TODO - you may try different values for the depth and look limits
	  Game g = new Game(3,0);
		boolean p1Turn = true;
		Solver p;
		Game.printGame();
		while (true){
			if (p1Turn)
				p = p1;
			else
				p = p2;
			if (Game.getNumMoves() == 0)
				break;
			b = Game.getBoard();
			a = p.selectMove(b);
			g.doMove(a);
			Game.printGame();
			p1Turn = !p1Turn;
		}
		if (g.p1Win())
			System.out.println("Player 1 wins!");
		else if (g.p2Win())
			System.out.println("Player 2 wins!");
		else
			System.out.println("Tie!");
	}
}
