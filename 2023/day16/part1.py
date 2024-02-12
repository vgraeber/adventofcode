from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  return rawinputarray

def movebeam(origarr, beamarr, dir, pos):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  beamreact = {'.': {'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W'}, '/': {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'}, '\\': {'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N'}, '|': {'N': 'N', 'S': 'S', 'E': ['N', 'S'], 'W': ['N', 'S']}, '-': {'N': ['E', 'W'], 'S': ['E', 'W'], 'E': 'E', 'W': 'W'}}
  beamopps = {'.': {'N': 'S','S': 'N','E': 'W','W': 'E'}, '/': {'N': 'W','S': 'E','E': 'S','W': 'N'}, '\\': {'N': 'E','S': 'W','E': 'N','W': 'S'}, '|': {'N': 'S','S': 'N','E': 'W','W': 'E'}, '-': {'N': 'S','S': 'N','E': 'W','W': 'E'}}
  arrbounds = {"row": [0, len(origarr)], "col": [0, len(origarr[0])]}
  currpos = origarr[pos[0]][pos[1]]
  if (beamarr[pos[0]][pos[1]][0] != '#'):
    beamarr[pos[0]][pos[1]][0] = '#'
    beamarr[pos[0]][pos[1]][1].append(dir)
  elif ((dir not in beamarr[pos[0]][pos[1]][1]) and (beamopps[currpos][dir] not in beamarr[pos[0]][pos[1]][1])):
    beamarr[pos[0]][pos[1]][1].append(dir)
  else:
    return
  dir = beamreact[currpos][dir]
  if (isinstance(dir, list)):
    pos1 = [(pos[0] + moveindir[dir[0]][0]), (pos[1] + moveindir[dir[0]][1])]
    pos2 = [(pos[0] + moveindir[dir[1]][0]), (pos[1] + moveindir[dir[1]][1])]
    if ((arrbounds["row"][0] <= pos1[0] < arrbounds["row"][1]) and (arrbounds["col"][0] <= pos1[1] < arrbounds["col"][1])):
      movebeam(origarr, beamarr, dir[0], pos1.copy())
    if ((arrbounds["row"][0] <= pos2[0] < arrbounds["row"][1]) and (arrbounds["col"][0] <= pos2[1] < arrbounds["col"][1])):
      movebeam(origarr, beamarr, dir[1], pos2.copy())
  else:
    pos[0] += moveindir[dir][0]
    pos[1] += moveindir[dir][1]
    if ((arrbounds["row"][0] <= pos[0] < arrbounds["row"][1]) and (arrbounds["col"][0] <= pos[1] < arrbounds["col"][1])):
      movebeam(origarr, beamarr, dir, pos.copy())

def calcenergized(beamarr):
  energized = 0
  for row in beamarr:
    for col in row:
      if (col[0] == '#'):
        energized += 1
  return energized

def printarr(arr, extra):
  toprint = ""
  for row in arr:
    for col in row:
      if extra:
        toprint += col[0]
      else:
        toprint += col
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  beamarray = [[['.', []] for col in row] for row in rawinputarray]
  movebeam(rawinputarray, beamarray, 'E', [0, 0])
  printarr(beamarray, True)
  energized = calcenergized(beamarray)
  print (energized)

main()
