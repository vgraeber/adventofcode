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
  for dir in arr[0][0].keys():
    arr[0][0][dir] = [[0, 0]]
  print (arr[0][0])

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
  editedposs = []
  for pos in nextposs:
    currdist = distarr[currpos[0][0]][currpos[0][1]][currpos[1]]
    for j in range(len(currdist)):
      currnodesdir = distarr[pos[0][0]][pos[0][1]][pos[2]]
      for i in range(len(currnodesdir)):
        adddist = origarr[pos[0][0]][pos[0][1]]
        newdist = currdist[j][0] + adddist
        currnode = currnodesdir[i]
        origcount = currnode[1]
        if (currnode[0] == "dist"):
          currnode = [newdist, pos[1]]
          editedposs.append(pos)
        elif ((newdist < currnode[0]) and (pos[1] < origcount)):
          currnode = [newdist, pos[1]]
          editedposs.append(pos)
        elif ((newdist < currnode[0]) or (pos[1] < origcount)):
          currnodesdir.append([newdist, pos[1]])
          editedposs.append(pos)
        elif ((newdist == currnode[0]) and (pos[1] < origcount)):
          currnode = [newdist, pos[1]]
          editedpos.append(pos)
        currnodesdir[i] = currnode
      distarr[pos[0][0]][pos[0][1]][pos[2]] = currnodesdir
  return editedposs

def notmapped(distarr, prevdistarr):
  for row in distarr:
    for col in row:
      for dir in col.values():
        for node in dir:
          if (node[0] == "dist"):
            return True
  if (distarr != prevdistarr):
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
  distarr = [[{'N': [["dist", "count"]], 'S': [["dist", "count"]], 'E': [["dist", "count"]], 'W': [["dist", "count"]]} for col in row] for row in rawinputarray]
  startpos = [0, 0]
  startcount = 0
  fixdistarrbounds(distarr)
  dest = [(len(rawinputarray) - 1), (len(rawinputarray[0]) - 1)]
  mapqueue = [[startpos, startcount, 'N']]
  prevdistarr = []
  while notmapped(distarr, prevdistarr):
    newmapqueue = []
    for poss in mapqueue:
      nextposs = movecruc(rawinputarray, poss[0], poss[2], poss[1])
      editedposs = editdistarr(rawinputarray, distarr, [poss[0], poss[2]], nextposs)
      for editedpos in editedposs:
        newmapqueue.append(editedpos)
    mapqueue = newmapqueue
    prevdistarr = distarr.copy()
  printarr(distarr)

main()
