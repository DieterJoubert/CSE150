
def is_complete(board): 
  last = -1
  for lst in board:
    for i in lst:
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

