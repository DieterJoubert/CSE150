__author__ = ’djoubert@ucsd.edu,student2@ucsd.edu,student3@ucsd.edu’

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
  print(is_complete(board))

if __name__ == '__main__':
  main()