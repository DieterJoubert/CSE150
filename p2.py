import Queue

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

  #for each position on the board
  for y in range(len(board)):
    for x in range(len(board[0])):
      check = board[y][x]

      if check == 0:
        continue

      #check all the positions in front of it and compare
      for y2 in range(y,len(board)):
        for x2 in range(x,len(board[0])):
          if board[y2][x2] and check > board[y2][x2]:
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
      if board[y][x] == 0
        return (y,x)

#breadth first search of the board for a solution
def bfs(board):
  direction = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}

  initial = board
  explored = []
  explored.append(board)

  #use a queue to BFS, put path of moves so far and board itself in queue
  tree = Queue.Queue()
  tree.put( ([],initial) )

  while tree.not_empty:
    (path,curr_board) = tree.get()

    #check if board is in finished position, in which case print path to get there
    if is_complete(curr_board):
      print path
      break

    else:
      zero = getzero(curr_board)







  





if __name__ == '__main__':
  main()
