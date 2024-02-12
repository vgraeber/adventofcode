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
  arrbounds = {"row": [0, len(origarr)], "col": [0, len(origarr[0])]}
  if (beamarr[pos[0]][pos[1]][0] != '#'):
    beamarr[pos[0]][pos[1]] = ['#', [dir]]
  elif (dir not in beamarr[pos[0]][pos[1]][1]):
    beamarr[pos[0]][pos[1]][1].append(dir)
  else:
    return
  pos[0] += moveindir[dir][0]
  pos[1] += moveindir[dir][1]
  currpos = origarr[pos[0]][pos[1]]
  dir = beamreact[currpos][dir]
  if ((pos[0] < arrbounds["row"][0]) or (arrbounds["row"][1] < pos[0]) or (pos[1] < arrbounds["col"][0]) or (arrbounds["col"][1] < pos[1])):
    return
  elif (isinstance(dir, list)):
    movebeam(origarr, beamarr, dir[0], pos)
    movebeam(origarr, beamarr, dir[1], pos)
  else:
    movebeam(origarr, beamarr, dir, pos)

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
  beamarray = [[['.']] * len(rawinputarray[0])] * len(rawinputarray)
  printarr(rawinputarray, False)
  printarr(beamarray, True)
  movebeam(rawinputarray, beamarray, 'E', [0, 0])
  printarr(beamarray, True)

main()
