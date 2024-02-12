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

def inbounds(origarr, pos):
  arrbounds = {"row": [0, len(origarr)], "col": [0, len(origarr[0])]}
  if ((arrbounds["row"][0] <= pos[0] < arrbounds["row"][1]) and (arrbounds["col"][0] <= pos[1] < arrbounds["col"][1])):
    return True
  return False

def movebeam(dir, pos):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  pos[0] += moveindir[dir][0]
  pos[1] += moveindir[dir][1]
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
    while not inbounds(origarr, pos):
      if (len(dirqueue) > 0):
        dir = dirqueue[0][0]
        pos = dirqueue[0][1]
        dirqueue.pop(0)
        pos = movebeam(dir, pos)
      else:
        return

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

def getbeamstartposs(origarr):
  startdir = {"row": {'0': 'S', str(len(origarr) - 1): 'N'}, "col": {'0': 'E', str(len(origarr[0]) - 1): 'W'}}
  startlocs = []
  startdirs = []
  for row in range(len(origarr)):
    for col in range(len(origarr[row])):
      if ((str(row) in startdir["row"]) and (str(col) in startdir["col"])):
        startlocs.append([row, col])
        startdirs.append(startdir["row"][str(row)])
        startlocs.append([row, col])
        startdirs.append(startdir["col"][str(col)])
      elif (str(row) in startdir["row"]):
        startlocs.append([row, col])
        startdirs.append(startdir["row"][str(row)])
      elif (str(col) in startdir["col"]):
        startlocs.append([row, col])
        startdirs.append(startdir["col"][str(col)])
  return startlocs, startdirs

def main():
  rawinputarray = getinput()
  startlocs, startdirs = getbeamstartposs(rawinputarray)
  beamarray = [[[['.', []] for col in row] for row in rawinputarray] for i in startlocs]
  energizedarrs = []
  for i in range(len(beamarray)):
    managebeam(rawinputarray, beamarray[i], startdirs[i], startlocs[i])
    energized = calcenergized(beamarray[i])
    energizedarrs.append(energized)
  print (max(energizedarrs))

main()
