from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  rawinputarray = [[int(col) for col in row] for row in rawinputarray]
  return rawinputarray

def rem(origlist, remele):
  try:
    origlist.remove(remele)
  except ValueError:
    pass

def getvaldirs(arr, currpos, prevdir, counter):
  oppdir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
  arrbounds = {"row": [0, (len(arr) - 1)], "col": [0, (len(arr[0]) - 1)]}
  dirs = ['N', 'E', 'S', 'W']
  remdir = oppdir.setdefault(prevdir, None)
  rem(dirs, remdir)
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

def movecruc(arr, currpos, prevdir, counter):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  valdirs = getvaldirs(arr, currpos, prevdir, counter)
  nextposs = []
  for dir in valdirs:
    posmove = moveindir[dir]
    nextpos = [[(currpos[0] + posmove[0]), (currpos[1] + posmove[1])]]
    if (dir != prevdir):
      nextpos.append(1)
    else:
      nextpos.append(counter + 1)
    nextpos.append(dir)
    nextposs.append(nextpos)
  return nextposs

def editdistarr(origarr, distarr, currpos, nextposs):
  currdist = distarr[currpos[0]][currpos[1]][0]
  editedposs = []
  for pos in nextposs:
    adddist = origarr[pos[0][0]][pos[0][1]]
    newdist = currdist + adddist
    currnode = distarr[pos[0][0]][pos[0][1]]
    if (currnode[0] == "dist"):
      currnode = [newdist, pos[1], pos[2]]
      editedposs.append(pos)
    elif (newdist < currnode[0]):
      currnode = [newdist, pos[1], pos[2]]
      editedposs.append(pos)
    elif (newdist == currnode[0]):
      origdir = currnode[2]
      if (not isinstance(origdir, list)):
        origdir = [origdir]
      if (pos[2] not in origdir):
        origdir.append(pos[2])
        currnode = [newdist, pos[1], origdir]
      print (currnode)
    distarr[pos[0][0]][pos[0][1]] = currnode
  return editedposs

def notmapped(distarr):
  for row in distarr:
    for col in row:
      if (col[0] == "dist"):
        return True
  return False

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += str(col)
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  printarr(rawinputarray)
  distarr = [[["dist", "count", "dir"] for col in row] for row in rawinputarray]
  startpos = [0, 0]
  startcount = 0
  distarr[0][0] = [0, startcount, None]
  dest = [(len(rawinputarray) - 1), (len(rawinputarray[0]) - 1)]
  mapqueue = [[startpos, startcount, None]]
  while notmapped(distarr):
    newmapqueue = []
    for poss in mapqueue:
      nextposs = movecruc(rawinputarray, poss[0], poss[2], poss[1])
      editedposs = editdistarr(rawinputarray, distarr, poss[0], nextposs)
      for editedpos in editedposs:
        newmapqueue.append(editedpos)
    mapqueue = newmapqueue
  printarr(distarr)

main()
