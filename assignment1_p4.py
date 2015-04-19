__author__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

import Queue
import copy
 
#check if board is in completed state
def is_complete(board):
  if board == []:
    return False
  last = -1
  for row in board:
    for i in row:
      if i == last+1:
        last = i
      else:
        return False
  return True

# takes board state, turns it into string, and hashes string to create unique int representation
def hash_fn(board):
  hash_string = ""
  for i in board:
    for j in i:
      hash_string += str(j)
  return hash(hash_string)

#gets the (y,x) coordinates of the 0 tile on the board
def getzero(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if(board[y][x] == 0):
                return (y,x)

#gets the maximum (y,x) coordinates a tile can be on the board
def yxmax(board):
    return(len(board) - 1, len(board[0]) - 1)
 
def dfsiterative(board):
    #since using LifoQueue (stack) for DFS, reverse direction list to retrieve Up first
    direction_FIFO = [ ('U', (-1,0)), ('D', (1,0)), ('L', (0,-1)), ('R', (0,1))]
    direction = direction_FIFO[::-1]
 
    initial = copy.deepcopy(board)
    MAX_DEPTH = 13
 
    # repeat DFS for each depth range
    for currdepth in range(MAX_DEPTH):

        tree = Queue.LifoQueue()
        tree.put( ([],initial,0) )
        explored = []
         
        while not tree.empty():
            (path,getboard,depth) = tree.get()
 
            # do not check if not at the depth counter for this iteration (i.e. leaf nodes)
            if depth == currdepth and is_complete(getboard):
                print "".join(path)
                return

            elif depth < currdepth:
                currboard = copy.deepcopy(getboard)
                explored.append(hash_fn(currboard))
                
                # check all four possible movement directions
                for(direct, (ydelt, xdelt)) in direction:
                    (yzero, xzero) = getzero(currboard)
                    (ymax, xmax) = yxmax(currboard)
 
                    # check if zero can be moved in this direction without going out of bound
                    if (0 <= yzero + ydelt <= ymax) and (0 <= xzero + xdelt <= xmax):
                        newboard = copy.deepcopy(currboard)
                        temp = int(newboard[yzero + ydelt][xzero + xdelt])
                        newboard[yzero + ydelt][xzero + xdelt] = 0
                        newboard[yzero][xzero] = temp
 
                        if hash_fn(newboard) not in explored:
                            newpath = path + [direct]
                            tree.put( (list(newpath), list(newboard), depth + 1) )

    #if can't find path, print unsolvable
    print "UNSOLVABLE"
    return
 
def main():
    import sys
    board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()] 
 
    if is_complete(board):
        print ""
    else:
        dfsiterative(board)

if __name__ == '__main__':
    main()