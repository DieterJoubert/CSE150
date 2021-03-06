import sys
import random
import copy

'''
run the program like this:

python genrandpuz.py [ysize] [xsize] [numofrandommoves]

the new puzzle will always write to a file called statout.txt
so we can call our p2-p5 stat files on statout.txt
'''

#gets the (y,x) coordinates of the 0 tile on the board
def getzero(board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      if board[y][x] == 0:
        return (y,x)

#gets the maximum (y,x) coordinates a tile can be on the board
def yxmax(board):
  return (len(board)-1, len(board[0])-1)

def createBoard(ysize, xsize):
    num = 0
    y = []

    for i in range(ysize):
        temp = []
        for j in range(xsize):
            temp.append(num)
            num = num + 1
        x = copy.deepcopy(temp)
        y.append(x)
    return y


#f = open(sys.argv[1], 'r+')
#board = [[int(n.strip()) for n in line.split(',')] for line in f.readlines()] 
ysize = int(sys.argv[1])
xsize = int(sys.argv[2])
numofmoves = int(sys.argv[3])
board = createBoard(ysize, xsize)

direction = [ ('U',(-1, 0)), ('D',(1, 0)), ('L',(0, -1)), ('R',(0, 1)) ]

for i in range(numofmoves):

    (y_zero, x_zero) = getzero(board)
    (y_max, x_max) = yxmax(board)
    inbounds = False

    while not inbounds:
        rand = random.randint(0,3)
        (name, (y_delta,x_delta)) = direction[rand]

        #check if zero can be moved in this direction (won't go out of bounds)
        if (0 <= y_zero + y_delta <= y_max) and (0 <= x_zero + x_delta <= x_max):
            inbounds = True
            temp = int(board[y_zero + y_delta][x_zero + x_delta])
            board[y_zero + y_delta][x_zero + x_delta] = 0
            board[y_zero][x_zero] = temp

line = ""
#f.close()

f = open("statout.txt", 'w')
for y in range(len(board)):
    line = str(board[y][0])
    for x in range(1, len(board[0])):
        line = line + "," + str(board[y][x])
    f.write(line + '\n')

f.close()