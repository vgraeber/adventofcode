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
      newrow.append(rawinputarray[row][col])
      if (col in emptycols):
        newrow.append('.')
    newinputarray.append(newrow)
    if (row in emptyrows):
      newinputarray.append(['.'] * (len(rawinputarray[row]) + len(emptycols)))
  return newinputarray

def getgalaxylocs(newinputarray):
  galaxylocs = []
  for line in range(len(newinputarray)):
    for char in range(len(newinputarray[line])):
      if (newinputarray[line][char] == '#'):
        galaxylocs.append([line, char])
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
