package Checkers;

/**
 * This contains an index into the board and an additional field to store a jumpCount (to
 * mark ordering in a sequence of pieces).
 * @author mhtong
 *
 */
public class Coord {
	/**The first coordinate*/
	public int x;
	
	/**The second coordinate*/
	public int y;
	
	/**An additional field able to be used to mark ordering in a sequence of pieces*/
	public int jumpCount;
	
	/**
	 * The constructor that fills all three fields (including jumpCount)
	 * @param x1 The first coordinate
	 * @param y1 The second coordinate
	 * @param jc The field able to be used to mark ordering in a sequence of pieces
	 */
	public Coord(int x1, int y1, int jc){
		x = x1;
		y = y1;
		jumpCount = jc;
	}
	
	/**
	 * The constructor that fills all three fields (including jumpCount)
	 * @param x1 The first coordinate
	 * @param y1 The second coordinate
	 */
	public Coord(int x1, int y1){
		x = x1;
		y = y1;
	}
	
	public boolean equals(Coord c1, Coord c2){
		if ((c1.x == c2.x) && (c1.y == c2.y))
			return true;
		return false;
	}

}
