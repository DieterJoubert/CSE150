import Queue
import copy

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

def getzero(board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      if board[y][x] == 0:
        return (y,x)

def yxmax(board):
  return (len(board)-1, len(board[0])-1)

def lengthwidth(board):
  return (len(board), len(board[0]))  

def print_board(board):
  for i in board:
    string = ""
    for j in i:
      string += " " + str(j)
    print string

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
  direction = [ ('U',(-1, 0)), ('D',(1, 0)), ('L',(0, -1)), ('R',(0, 1)) ]

  initial = board
  explored = []
  explored.append(list(board))

  (length, width) = lengthwidth(board)
  solved_board = []
  index = 0
  for i in range(length):
    row = []
    for j in range(width):
      row.append(index)
      index += 1
    solved_board.append(row)

  #use a LIFO queue to DFS, put path of moves so far and board itself in queue
  tree = Queue.PriorityQueue()
  h_start = calc_h(initial,solved_board)
  tree.put( (0 + h_start, ([],initial,0)) )

  while not tree.empty():
    (priority, (path,get_board,depth)) = tree.get()
    print str(priority) + "  " + " ".join(path)

    #check if board is in finished position, in which case print path to get there
    if is_complete(get_board):
      print "".join(path)
      return

    else:
      for (name, (y_delta,x_delta)) in direction:
        #TODO: doble check direction is ok

        curr_board = copy.deepcopy(get_board)
        (y_zero, x_zero) = getzero(curr_board)
        (y_max, x_max) = yxmax(curr_board)

        #check if zero can be moved in this direction (won't go out of bounds)
        if (0 <= y_zero + y_delta <= y_max) and (0 <= x_zero + x_delta <= x_max):

          #switch zero with element in that direction
          new_board = copy.deepcopy(curr_board)
          temp = int(new_board[y_zero+y_delta][x_zero+x_delta])
          new_board[y_zero+y_delta][x_zero+x_delta] = 0
          new_board[y_zero][x_zero] = temp

          if new_board not in explored:
            explored.append(list(curr_board))
            new_path = path + [name]
            new_depth = depth + 1
            f_value = new_depth + calc_h(new_board, solved_board)

            tree.put( (f_value, (list(new_path), list(new_board), new_depth)) )


  print "UNSOLVABLE"
  return

if __name__ == '__main__':
  main()
