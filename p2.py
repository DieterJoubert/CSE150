import Queue
import copy

def is_complete(board):
  if board == []:
    return False
  last = -1
  for lst in board:
    for i in lst:
      if i == last+1:
        last = i
      else:
        return False
  return True


#check the number of inversions, if odd, not solvable
def is_solvable(board):
  inv_count = 0

  nums = []
  #for each position on the board
  for y in range(len(board)):
    for x in range(len(board[0])):
      check = board[y][x]

      if check != 0:
        nums.append(check)

  for i in range(len(nums)):
    for j in range(i,len(nums)):
      if nums[i] > nums[j]:
        inv_count += 1

  #if odd number of inversions, cannot be solved, else can be
  if (inv_count % 2 == 1):
    return False
  else:
    return True

def main():
  import sys
  board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()] 

  #check if board can't be solved, in which case end main, print UNSOLVABLE
  if not is_solvable(board):
    print("UNSOLVABLE")

  #check if board finished, in which case don't print anything, end main
  elif is_complete(board):
    print ""
  
  else:
    bfs(board)

def getzero(board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      if board[y][x] == 0:
        return (y,x)

def lengthwidth(board):
  return (len(board)-1, len(board[0])-1)

def print_board(board):
  for i in board:
    string = ""
    for j in i:
      string += " " + str(j)
    print string

#breadth first search of the board for a solution
def bfs(board):
  direction = [ ('U',(-1, 0)), ('R',(0, 1)), ('D',(1, 0)), ('L',(0, -1))]

  initial = board
  explored = []
  explored.append(list(board))

  #use a queue to BFS, put path of moves so far and board itself in queue
  tree = Queue.Queue()
  tree.put( ([],initial) )

  while not tree.empty():
    (path,get_board) = tree.get()

    #check if board is in finished position, in which case print path to get there
    if is_complete(get_board):
      print "".join(path)
      break

    else:
      for (name, (y_delta,x_delta)) in direction:

        curr_board = copy.deepcopy(get_board)
        (y_zero, x_zero) = getzero(curr_board)
        (y_max, x_max) = lengthwidth(curr_board)

        #check if zero can be moved in this direction (won't go out of bounds)
        if (y_zero + y_delta <= y_max) and (x_zero + x_delta <= x_max):

          #switch zero with element in that direction
          new_board = copy.deepcopy(curr_board)
          temp = int(new_board[y_zero+y_delta][x_zero+x_delta])
          new_board[y_zero+y_delta][x_zero+x_delta] = 0
          new_board[y_zero][x_zero] = temp

          if new_board not in explored:
            explored.append(list(curr_board))
            new_path = path + [name]
            tree.put( (list(new_path), list(new_board)) )


if __name__ == '__main__':
  main()
