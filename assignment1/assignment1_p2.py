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
      if board[y][x] == 0:
        return (y,x)

#gets the maximum (y,x) coordinates a tile can be on the board
def yxmax(board):
  return (len(board)-1, len(board[0])-1)

#breadth first search of the board for a solution
def bfs(board):
  direction = [ ('U',(-1, 0)), ('D',(1, 0)), ('L',(0, -1)), ('R',(0, 1)) ]

  initial = board
  explored = []
  
  #use a queue to BFS, put path of moves so far and board itself in queue
  tree = Queue.Queue()
  tree.put( ([],initial) )

  while not tree.empty():
    (path,get_board) = tree.get()

    #check if board is in finished position, in which case print path to get there
    if is_complete(get_board):
      print "".join(path)
      return

    else:
      curr_board = copy.deepcopy(get_board)
      explored.append(hash_fn(curr_board))

      # check all four possible movement directions
      for (name, (y_delta,x_delta)) in direction:

        (y_zero, x_zero) = getzero(curr_board)
        (y_max, x_max) = yxmax(curr_board)

        #check if zero can be moved in this direction (won't go out of bounds)
        if (0 <= y_zero + y_delta <= y_max) and (0 <= x_zero + x_delta <= x_max):

          #switch zero with element in that direction
          new_board = copy.deepcopy(curr_board)
          temp = int(new_board[y_zero+y_delta][x_zero+x_delta])
          new_board[y_zero+y_delta][x_zero+x_delta] = 0
          new_board[y_zero][x_zero] = temp

          if hash_fn(new_board) not in explored:
            new_path = path + [name]
            tree.put( (list(new_path), list(new_board)) )

  #if no path to solution was found
  print "UNSOLVABLE"
  return

def main():
  import sys
  board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()] 

  #check if board finished, in which case don't print anything, end main
  if is_complete(board):
    print ""
  
  else:
    bfs(board)  

if __name__ == '__main__':
  main()
