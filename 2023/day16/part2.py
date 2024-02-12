from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  return rawinputarray

def getnewbeamdir(origarr, beamarr, dir, pos):
  newbeamdir = {'.': {'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W'}, '/': {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'}, '\\': {'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N'}, '|': {'N': 'N', 'S': 'S', 'E': ['N', 'S'], 'W': ['N', 'S']}, '-': {'N': ['E', 'W'], 'S': ['E', 'W'], 'E': 'E', 'W': 'W'}}
  oppdir = {'.': {'N': 'S','S': 'N','E': 'W','W': 'E'}, '/': {'N': 'W','S': 'E','E': 'S','W': 'N'}, '\\': {'N': 'E','S': 'W','E': 'N','W': 'S'}, '|': {'N': 'S','S': 'N','E': 'W','W': 'E'}, '-': {'N': 'S','S': 'N','E': 'W','W': 'E'}}
  currpos = origarr[pos[0]][pos[1]]
  if (beamarr[pos[0]][pos[1]][0] != '#'):
    beamarr[pos[0]][pos[1]][0] = '#'
    beamarr[pos[0]][pos[1]][1].append(dir)
  elif ((dir not in beamarr[pos[0]][pos[1]][1]) and (oppdir[currpos][dir] not in beamarr[pos[0]][pos[1]][1])):
    beamarr[pos[0]][pos[1]][1].append(dir)
  else:
    return None
  dir = newbeamdir[currpos][dir]
  return dir

def movebeam(dir, pos):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  pos[0] += moveindir[dir][0]
  pos[1] += moveindir[dir][1]
  return pos

def inbounds(origarr, pos):
  arrbounds = {"row": [0, len(origarr)], "col": [0, len(origarr[0])]}
  if ((arrbounds["row"][0] <= pos[0] < arrbounds["row"][1]) and (arrbounds["col"][0] <= pos[1] < arrbounds["col"][1])):
    return True
  return False

def adjustpos(origarr, pos):
  arrbounds = {"row": [0, len(origarr)], "col": [0, len(origarr[0])]}
  if (pos[0] < arrbounds["row"][0]):
    pos[0] = arrbounds["row"][1] + pos[0]
  elif (arrbounds["row"][1] <= pos[0]):
    pos[0] = pos[0] - arrbounds["row"][1]
  if (pos[1] < arrbounds["col"][0]):
    pos[1] = arrbounds["col"][1] + pos[1]
  elif (arrbounds["col"][1] <= pos[1]):
    pos[1] = pos[1] - arrbounds["col"][1]
  return pos

def managebeam(origarr, beamarr, dir, pos):
  dirqueue = []
  while dir is not None:
    dir = getnewbeamdir(origarr, beamarr, dir, pos)
    if isinstance(dir, list):
      dirqueue.append([dir[1], pos.copy()])
      dir = dir[0]
    elif dir is None:
      if (len(dirqueue) > 0):
        dir = dirqueue[0][0]
        pos = dirqueue[0][1]
        dirqueue.pop(0)
      else:
        return
    pos = movebeam(dir, pos)
    if not inbounds(origarr, pos):
      pos = adjustpos(origarr, pos)

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
  managebeam(rawinputarray, beamarray, 'E', [0, 0])
  printarr(beamarray, True)
  energized = calcenergized(beamarray)
  print (energized)

main()
