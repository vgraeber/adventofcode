from pathlib import Path
import copy

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
  arr[0][0][None] = [{"dist": 0, "count": 0}]

def notmapped(distarr, prevdistarr):
  if (distarr != prevdistarr):
    return True
  return False

def rem(origlist, remele):
  try:
    origlist.remove(remele)
  except ValueError:
    pass

def getvaldirs(arr, currpos, prevdir, counter):
  oppdirs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
  arrbounds = {"row": [0, (len(arr) - 1)], "col": [0, (len(arr[0]) - 1)]}
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

def movecruc(arr, poss, distarr):
  moveindir = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  valdirs = getvaldirs(arr, poss["currpos"], poss["prevdir"], poss["count"])
  nextposs = []
  for dir in valdirs:
    posmove = moveindir[dir]
    nextpos = {}
    nextpos["currpos"] = [(poss["currpos"][0] + posmove[0]), (poss["currpos"][1] + posmove[1])]
    if (dir != poss["prevdir"]):
      nextpos["count"] = 1
    else:
      nextpos["count"] = poss["count"] + 1
    nextpos["prevdir"] = dir
    nextpos["prevdist"] = poss["prevdist"]
    nextposs.append(nextpos)
  return nextposs

def remdupes(nodes):
  newnodes = []
  for n in nodes:
    if (n not in newnodes):
      newnodes.append(n)
  return newnodes

def editdistarr(origarr, distarr, currpos, nextposs):
  editedposs = []
  currdist = distarr[currpos["currpos"][0]][currpos["currpos"][1]][currpos["prevdir"]]
  for pos in nextposs:
    for j in range(len(currdist)):
      currnodesdir = distarr[pos["currpos"][0]][pos["currpos"][1]][pos["prevdir"]]
      adddist = origarr[pos["currpos"][0]][pos["currpos"][1]]
      pos["prevdist"] += adddist
      newnode = {"dist": pos["prevdist"], "count": pos["count"]}
      if (len(currnodesdir) == 1):
        currnode = currnodesdir[0]
        if (currnode["dist"] is None):
          currnode = newnode
          if (pos not in editedposs):
            editedposs.append(pos)
        elif (((newnode["dist"] <= currnode["dist"]) and (newnode["count"] <= currnode["count"])) and ((newnode["dist"] < currnode["dist"]) or (newnode["count"] < currnode["count"]))):
          currnode = newnode
          if (pos not in editedposs):
            editedposs.append(pos)
        elif ((newnode["dist"] < currnode["dist"]) or (newnode["count"] < currnode["count"])):
          if (pos not in editedposs):
            currnodesdir.append(newnode)
            editedposs.append(pos)
        currnodesdir[0] = currnode
      else:
        for i in range(len(currnodesdir)):
          currnode = currnodesdir[i]
          if (((newnode["dist"] <= currnode["dist"]) and (newnode["count"] <= currnode["count"])) and ((newnode["dist"] < currnode["dist"]) or (newnode["count"] < currnode["count"]))):
            currnode = newnode
            if (pos not in editedposs):
              editedposs.append(pos)
        for i in range(len(currnodesdir)):
          if ((newnode["dist"] < currnode["dist"]) or (newnode["count"] < currnode["count"])):
            if (pos not in editedposs):
              currnodesdir.append(newnode)
              editedposs.append(pos)
        currnodesdir[i] = currnode
      currnodesdir = remdupes(currnodesdir)
      distarr[pos["currpos"][0]][pos["currpos"][1]][pos["prevdir"]] = currnodesdir
  return editedposs

def runthroughcity(rawinputarray, distarr):
  startpos = [0, 0]
  startcount = 0
  startdist = 0
  mapqueue = [{"currpos": startpos, "count": startcount, "prevdir":  None, "prevdist": startdist}]
  prevdistarr = []
  while notmapped(distarr, prevdistarr):
    newmapqueue = []
    prevdistarr = copy.deepcopy(distarr)
    for poss in mapqueue:
      nextposs = movecruc(rawinputarray, poss, distarr)
      editedposs = editdistarr(rawinputarray, distarr, poss, nextposs)
      for editedpos in editedposs:
        if (editedpos not in newmapqueue):
          newmapqueue.append(editedpos)
    mapqueue = newmapqueue

def main():
  rawinputarray = getinput()
  printarr(rawinputarray)
  distarr = [[{'N': [{"dist": None, "count": None}], 'S': [{"dist": None, "count": None}], 'E': [{"dist": None, "count": None}], 'W': [{"dist": None, "count": None}]} for col in row] for row in rawinputarray]
  fixdistarrbounds(distarr)
  runthroughcity(rawinputarray, distarr)
  print (distarr[-1][-1])

main()
