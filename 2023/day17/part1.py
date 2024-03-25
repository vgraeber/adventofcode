from pathlib import Path
import copy

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  rawinputarray = [[int(col) for col in row] for row in rawinputarray]
  return rawinputarray

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += str(col)
    toprint += "\n"
  print (toprint)

def fixdistarrbounds(arr):
  arrbounds = {"row": [0, (len(arr) - 1)], "col": [0, (len(arr[0]) - 1)]}
  for r in range(len(arr)):
    for c in range(len(arr[r])):
      if (r == arrbounds["row"][0]):
        arr[r][c].pop('S')
      elif (r == arrbounds["row"][1]):
        arr[r][c].pop('N')
      if (c == arrbounds["col"][0]):
        arr[r][c].pop('E')
      elif (c == arrbounds["col"][1]):
        arr[r][c].pop('W')
  arr[0][0][None] = {0: 0}

def notmapped(distarr, prevdistarr):
  if (distarr != prevdistarr):
    return True
  return False

def rem(origlist, remele):
  try:
    origlist.remove(remele)
  except ValueError:
    pass

def getvaldirs(arrbounds, currpos, prevdir, counter):
  oppdirs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
  dirs = ['N', 'E', 'S', 'W']
  oppdir = oppdirs.setdefault(prevdir, None)
  rem(dirs, oppdir)
  if (counter == 3):
    rem(dirs, prevdir)
  if (currpos[0] == arrbounds["row"][0]):
    rem(dirs, 'N')
  elif (currpos[0] == arrbounds["row"][1]):
    rem(dirs, 'S')
  if (currpos[1] == arrbounds["col"][0]):
    rem(dirs, 'W')
  elif (currpos[1] == arrbounds["col"][1]):
    rem(dirs, 'E')
  return dirs

def movecruc(arrbounds, poss):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  currpos = poss["currpos"]
  valdirs = getvaldirs(arrbounds, currpos, poss["prevdir"], poss["count"])
  nextposs = []
  for dir in valdirs:
    posmove = moveindir[dir]
    nextpos = copy.deepcopy(poss)
    nextpos["currpos"][0] += posmove[0]
    nextpos["currpos"][1] += posmove[1]
    if (dir != poss["prevdir"]):
      nextpos["count"] = 1
      nextpos["prevdir"] = dir
    else:
      nextpos["count"] += 1
    nextposs.append(nextpos)
  return nextposs

def editdistarr(origarr, distarr, currpos, nextposs):
  editedposs = []
  currdist = distarr[currpos["currpos"][0]][currpos["currpos"][1]][currpos["prevdir"]]
  for pos in nextposs:
    currdist = distarr[pos["currpos"][0]][pos["currpos"][1]][pos["prevdir"]][pos["count"]]
    adddist = origarr[pos["currpos"][0]][pos["currpos"][1]]
    newdist = pos["prevdist"] + adddist
    canappend = False
    if (currdist is None):
      distarr[pos["currpos"][0]][pos["currpos"][1]][pos["prevdir"]][pos["count"]] = newdist
      canappend = True
    elif (newdist < currdist):
      distarr[pos["currpos"][0]][pos["currpos"][1]][pos["prevdir"]][pos["count"]] = newdist
      canappend = True
    if (canappend):
      pos["prevdist"] += adddist
      if (pos not in editedposs):
        editedposs.append(pos)
  return editedposs

def runthroughcity(arr, distarr):
  arrbounds = {"row": [0, (len(arr) - 1)], "col": [0, (len(arr[0]) - 1)]}
  mapqueue = [{"currpos": [0, 0], "count": 0, "prevdir":  None, "prevdist": 0}]
  prevdistarr = []
  while notmapped(distarr, prevdistarr):
    newmapqueue = []
    prevdistarr = copy.deepcopy(distarr)
    for poss in mapqueue:
      nextposs = movecruc(arrbounds, poss)
      editedposs = editdistarr(arr, distarr, poss, nextposs)
      for editedpos in editedposs:
        if (editedpos not in newmapqueue):
          newmapqueue.append(editedpos)
    mapqueue = newmapqueue

def printdistarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += str(col)
      toprint += "\n"
    toprint += "\n\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  #printarr(rawinputarray)
  distarr = [[{'N': {1: None, 2: None, 3: None}, 'S': {1: None, 2: None, 3: None}, 'E': {1: None, 2: None, 3: None}, 'W': {1: None, 2: None, 3: None}} for col in row] for row in rawinputarray]
  fixdistarrbounds(distarr)
  runthroughcity(rawinputarray, distarr)
  print(distarr[-1][-1])

main()
