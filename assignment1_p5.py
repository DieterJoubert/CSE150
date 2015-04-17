import Queue
import copy
from heapq import *

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

def main():
  import sys
  board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()] 

  if is_complete(board):
    print ""
  
  else:
    a_star(board)

def hash_fn(board):
  hash_string = ""
  for i in board:
    for j in i:
      hash_string += str(j)
  return hash(hash_string)    

def getzero(board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      if board[y][x] == 0:
        return (y,x)

def yxmax(board):
  return (len(board)-1, len(board[0])-1)

def lengthwidth(board):
  return (len(board), len(board[0]))  

def calc_h(check_board, solved_board):
  h = 0

  coordinates = {}

  for y in range(len(check_board)):
    for x in range(len(check_board[0])):
      coordinates[check_board[y][x]] = (y, x)

  for y_solved in range(len(solved_board)):
    for x_solved in range(len(solved_board[0])):
      value = solved_board[y_solved][x_solved]
      (y_start, x_start) = coordinates[value]

      h += abs(y_start - y_solved)
      h += abs(x_start - x_solved)

  return h

#breadth first search of the board for a solution
def a_star(board):
  directionOLD = [ ('U',(-1, 0)), ('D',(1, 0)), ('L',(0, -1)), ('R',(0, 1)) ]
  direction = directionOLD

  weightOLD = {'U': 1, 'D': 2, 'L': 3, 'R': 4}
  weight = {'U': 4, 'D': 3, 'L': 2, 'R': 1}

  initial = copy.deepcopy(board)
  explored = []
  explored.append( hash_fn(board) )

  #create solved board to check against for heuristic
  (length, width) = lengthwidth(board)
  solved_board = []
  index = 0
  for i in range(length):
    row = []
    for j in range(width):
      row.append(index)
      index += 1
    solved_board.append(row)

  tree = []
  h_start = calc_h(initial,solved_board)
  heappush(tree, (0 + h_start, 0, [], initial, 0) )

  while len(tree):
    ( (priority, priority_extra, path, get_board, depth) ) = heappop(tree)

    #check if board is in finished position, in which case print path to get there
    if is_complete(get_board):
      print "".join(path)
      return

    else:
      curr_board = copy.deepcopy(get_board)
      explored.append( hash_fn(curr_board) )
      
      for (name, (y_delta,x_delta)) in direction:
        #TODO: doble check direction is ok

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
            new_path = list(path) + [name]
            new_depth = depth + 1
            f_value = new_depth + calc_h(new_board, solved_board)
            priority_second = weight[name]
            heappush(tree, (f_value, priority_second, list(new_path), new_board, new_depth) )

  print "UNSOLVABLE"
  return

if __name__ == '__main__':
  main()
