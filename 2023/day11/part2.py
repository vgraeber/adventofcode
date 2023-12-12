from pathlib import Path
import numpy as np

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = np.array([list(line) for line in rawinputlist])
  return rawinputarray

def getemptyspace(rawinputarray):
  emptyrows = []
  emptycols = []
  for row in range(len(rawinputarray)):
    if (rawinputarray[row] == (['.'] * len(rawinputarray[row]))).all():
      emptyrows.append(row)
  for col in range(len(rawinputarray[0])):
    if (rawinputarray[:, col] == (['.'] * len(rawinputarray[:, col]))).all():
      emptycols.append(col)
  return emptyrows, emptycols

def expandgalaxy(rawinputarray):
  emptyrows, emptycols = getemptyspace(rawinputarray)
  newinputarray = []
  for row in range(len(rawinputarray)):
    newrow = []
    for col in range(len(rawinputarray[row])):
      if (col in emptycols):
        newrow.append('*')
      else:
        newrow.append(rawinputarray[row][col])
    if (row in emptyrows):
      newinputarray.append(['*'] * (len(rawinputarray[row]) + len(emptycols)))
    else:
      newinputarray.append(newrow)
  return newinputarray

def getgalaxylocs(newinputarray):
  galaxylocs = []
  lineexpands = 0
  colexpands = 0
  expandval = 1000000
  for line in range(len(newinputarray)):
    if (newinputarray[line] == (['*'] * len(newinputarray[line]))):
      lineexpands += 1
    for char in range(len(newinputarray[line])):
      if (newinputarray[line][char] == '*'):
        colexpands += 1
      if (newinputarray[line][char] == '#'):
        galaxylocs.append([(line + (lineexpands * (expandval - 1))), (char + (colexpands * (expandval - 1)))])
    colexpands = 0
  return galaxylocs

def getdists(galaxylocs):
  dists = []
  for i in range(len(galaxylocs)):
    for j in range(1, len(galaxylocs) - i):
      curr = galaxylocs[i]
      next = galaxylocs[i + j]
      dists.append(abs(next[0] - curr[0]) + abs(next[1] - curr[1]))
  return dists

def main():
  rawinputarray = getinput()
  newinputarray = expandgalaxy(rawinputarray)
  galaxylocs = getgalaxylocs(newinputarray)
  dists = getdists(galaxylocs)
  print (sum(dists))

main()
