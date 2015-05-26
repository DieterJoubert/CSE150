import subprocess
import numpy as np
from collections import defaultdict
from time import time 

### Can tune these parameters
max_size = 6 # 4-8
max_difficulty = 3 # 0-3
reps = 2
startBoardInd = 1
numBoards = 3
#########

size = defaultdict(list)
log = open("logs.txt", 'w')

print "Running tests"

for s in range(4, max_size + 1): #go through all sizes
  print "On size " + str(s)

  for d in range(max_difficulty + 1): #go through all difficulties for each size
    print "\tdifficulty " + str(d)

    for b in range(startBoardInd, numBoards + startBoardInd): #go through numBoards boards for each size and difficulty
      print "\t\tboard ID " + str(b)
      curr_board = open("curr_board.txt", 'w')
      command = "python fetch_puzzle.py " + str(s) + " " + str(d) + " " + str(b)
      fetch = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      out, err = fetch.communicate()
      curr_board.write(out)
      curr_board.close()

      for r in range(reps): #average over this many reps per board per difficulty per size
        print "\t\t\trep " + str(r)        

        run = subprocess.Popen("python solve_puzzle.py < curr_board.txt", stdout=subprocess.PIPE, shell=True)
        out, err = run.communicate()
        log.write("size = " + str(s) + " difficulty = " + str(d) + " boardID = " + str(b) + " rep = " + str(r) + '\n')
        log.write(out + "'\n---------------------------------\n'")
        seconds = out.split('k ')[1]
        time = float(seconds.split(' ')[0])

        size[str(s) + str(d)].append(time)

log.close()

print "Tests Complete\n"

results = open("analysis.txt", 'w')

print "Writing Results\n"

for k in sorted(size.keys()):
  sd = list(k)
  m = np.mean(np.asarray(size[k]))
  results.write("size = " + str(sd[0]) + " difficulty = " + str(sd[1]) + " mean time = " + str(m) + '\n')

results.close()
print "SUCCESS!"