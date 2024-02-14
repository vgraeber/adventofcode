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

def move(pos, dir, mult):
  moveindir = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
  pos[0] += moveindir[dir][0] * mult
  pos[1] += moveindir[dir][1] * mult
  return pos

def getarrsize(inputarr):
  pos = [0, 0]
  top = 0
  bott = 0
  left = 0
  right = 0
  for line in inputarr:
    pos = move(pos, line[0], int(line[1]))
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
  startpos = [pos[0] - top, pos[1] - left]
  return numrows, numcols, startpos

def dig(diginst, digarr, pos):
  digarr[pos[0]][pos[1]] = '#'
  for line in diginst:
    for i in range(int(line[1])):
      pos = move(pos, line[0], 1)
      digarr[pos[0]][pos[1]] = '#'
  printarr(digarr)

def fill(digarr):
  for row in range(len(digarr)):
    inside = False
    state = '.'
    for col in range(len(digarr[row])):
      if ((state != '#') and (digarr[row][col] != state)):
        inside = not inside
        state = digarr[row][col]
      if inside:
        digarr[row][col] = '#'
  printarr(digarr)

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += col
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  numrows, numcols, startpos = getarrsize(rawinputarray)
  digarr = [['.' for col in range(numcols)] for row in range(numrows)]
  dig(rawinputarray, digarr, startpos)
  fill(digarr)

main()
