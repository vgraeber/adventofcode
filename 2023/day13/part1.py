from pathlib import Path
import numpy as np

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlists = rawinput.split("\n\n")
  rawinputlist = [arr.split("\n") for arr in rawinputlists]
  rawinputlist[-1].pop()
  rawinputarray = [np.array([list(line) for line in arr]) for arr in rawinputlist]
  return rawinputarray

def getvertmirror(rawinputarray):
  maxreflect = len(rawinputarray[0]) // 2
  for col in range(1, (len(rawinputarray[0]) - 1)):
    leftbound = col - maxreflect
    rightbound = col + maxreflect
    if (leftbound < 0):
      leftbound = 0
      rightbound = 2 * col
    if (rightbound > len(rawinputarray[0])):
      rightbound = len(rawinputarray[0])
      leftbound = rightbound - (2 * (rightbound - col))
    mirror = True
    for row in range(len(rawinputarray)):
      left = ''.join(rawinputarray[row][leftbound:col])
      right = ''.join(rawinputarray[row][col:rightbound])
      right = right[::-1]
      if (left != right):
        mirror = False
        break
    if (mirror):
      return col

def gethorizmirror(rawinputarray):
  maxreflect = len(rawinputarray) // 2
  for row in range(1, (len(rawinputarray) - 1)):
    upperbound = row - maxreflect
    lowerbound = row + maxreflect
    if (upperbound < 0):
      upperbound = 0
      lowerbound = 2 * row
    if (lowerbound > len(rawinputarray)):
      lowerbound = len(rawinputarray)
      upperbound = lowerbound - (2 * (lowerbound - row))
    mirror = True
    for col in range(len(rawinputarray[row])):
      upper = ''.join(rawinputarray[:, col][upperbound:row])
      lower = ''.join(rawinputarray[:, col][row:lowerbound])
      lower = lower[::-1]
      if (upper != lower):
        mirror = False
        break
    if (mirror):
      return row

def printarr(arr):
  toprint = ""
  for block in arr:
    print (block)
    for row in block:
      print (row)
      for col in row:
        toprint += col
      toprint += "\n"
    toprint += "\n"
  print (toprint)

def getsumm(vertmirrors, horizmirrors):
  vertsum = 0
  horizsum = 0
  for i in vertmirrors:
    if (i is not None):
      vertsum += i
  for i in horizmirrors:
    if (i is not None):
      horizsum += 100 * i
  return (vertsum + horizsum)

def main():
  rawinputarrays = getinput()
  vertmirrors = []
  horizmirrors = []
  for arr in rawinputarrays:
    vertmirror = getvertmirror(arr)
    horizmirror = gethorizmirror(arr)
    vertmirrors.append(vertmirror)
    horizmirrors.append(horizmirror)
  summ = getsumm(vertmirrors, horizmirrors)
  print (summ)

main()
