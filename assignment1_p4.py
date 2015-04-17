import Queue
import copy
 
def is_complete(board):
    if board == []:
        return False
    last = -1
    for lst in board:
        for i in lst:
            if i == last + 1:
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
        dfsiterative(board)

def hash_fn(board):
  hash_string = ""
  for i in board:
    for j in i:
      hash_string += str(j)
  return hash(hash_string)
 
def getzero(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if(board[y][x] == 0):
                return (y,x)
 
def yxmax(board):
    return(len(board) - 1, len(board[0]) - 1)
 
def dfsiterative(board):
    direction = [ ('U', (-1,0)), ('D', (1,0)), ('L', (0,-1)), ('R', (0,1))]
 
    initial = board
    MAX_DEPTH = 13
 
    for currdepth in range(MAX_DEPTH):
        tree = Queue.Queue()
        tree.put( ([],initial,0) )
        explored = []
        
        #explored.append(list(board))
 
        while not tree.empty():
            (path,getboard,depth) = tree.get()
 
            if is_complete(getboard):
                print "".join(path)
                return
 
            elif depth < currdepth:
                currboard = copy.deepcopy(getboard)
                explored.append(hash_fn(currboard))
                
                for(direct, (ydelt, xdelt)) in direction:
                    (yzero, xzero) = getzero(currboard)
                    (ymax, xmax) = yxmax(currboard)
 
                    if (0 <= yzero + ydelt <= ymax) and (0 <= xzero + xdelt <= xmax):
                        newboard = copy.deepcopy(currboard)
                        temp = int(newboard[yzero + ydelt][xzero + xdelt])
                        newboard[yzero + ydelt][xzero + xdelt] = 0
                        newboard[yzero][xzero] = temp
 
                        if hash_fn(newboard) not in explored:
                            newpath = path + [direct]
                            tree.put( (list(newpath), list(newboard), depth + 1) )
    print "UNSOLVABLE"
    return
 
if __name__ == '__main__':
    main()