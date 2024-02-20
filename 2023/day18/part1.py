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

def gettypecorner(diginst, instnum):
  cornerchange = {'U': {'L': '7', 'R': 'F'}, 'D': {'L': 'J','R': 'L'}, 'L': {'U': 'L', 'D': 'F'}, 'R': {'U': 'J', 'D': '7'}}
  prevline = diginst[instnum - 1]
  currline = diginst[instnum]
  return cornerchange[prevline[0]][currline[0]]

def dig(diginst, digarr, pos):
  for instnum in range(len(diginst)):
    line = diginst[instnum]
    corner = gettypecorner(diginst, instnum)
    digarr[pos[0]][pos[1]] = corner
    for i in range(int(line[1])):
      pos = move(pos, line[0], 1)
      digarr[pos[0]][pos[1]] = '#'
  corner = gettypecorner(diginst, 0)
  digarr[pos[0]][pos[1]] = corner
  printarr(digarr)

def fill(digarr):
  cornerpairs = {'F': {'J': True, '7': False}, 'L': {'7': True,'J': False}}
  for row in range(len(digarr)):
    inside = False
    toggs = ['#', 'F', '7', 'J', 'L']
    corns = ['F', '7', 'J', 'L']
    corner = False
    startcorner = ''
    endcorner = ''
    for col in range(len(digarr[row])):
      pos = digarr[row][col]
      if (pos in toggs):
        if (pos in corns):
          corner = not corner
          if not corner:
            endcorner = pos
            if cornerpairs[startcorner][endcorner]:
              inside = not inside
          else:
            startcorner = pos
        elif (not corner):
          inside = not inside
      if (inside and (pos not in corns)):
        digarr[row][col] = '#'
  printarr(digarr)

def calcvol(digarr):
  vol = 0
  for row in digarr:
    for col in row:
      pool = ['#', 'F', '7', 'J', 'L']
      if (col in pool):
        vol += 1
  print (vol)

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += col[0]
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  numrows, numcols, startpos = getarrsize(rawinputarray)
  digarr = [['.' for col in range(numcols)] for row in range(numrows)]
  dig(rawinputarray, digarr, startpos)
  fill(digarr)
  calcvol(digarr)

main()
