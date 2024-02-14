from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [line.split(' ') for line in rawinputlist]
  return rawinputarray

def getarrsize(inputarr):
  pos = [0, 0]
  top = 0
  bott = 0
  left = 0
  right = 0
  moveindir = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
  for line in inputarr:
    pos[0] += moveindir[line[0]][0] * int(line[1])
    pos[1] += moveindir[line[0]][1] * int(line[1])
    if (pos[0] < top):
      top = pos[0]
    if (bott < pos[0]):
      bott = pos[0]
    if (pos[1] < left):
      left = pos[1]
    if (right < pos[1]):
      right = pos[1]
  numrows = bott - top + 1
  numcols = right - left + 1
  return numrows, numcols

def dig(diginst, digarr, dir, pos):
  moveindir = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += col
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  numrows, numcols = getarrsize(rawinputarray)
  print (numrows, numcols)

main()
