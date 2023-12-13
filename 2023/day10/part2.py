from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample5.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  return rawinputarray

def findstartingpos(rawinputarray):
  for line in range(len(rawinputarray)):
    for char in range(len(rawinputarray[line])):
      if (rawinputarray[line][char] == 'S'):
        return [line, char]

def findpipedict(startingpos, rawinputarray):
  pipes = {
    '|': {'N': True, 'S': True, 'E': False, 'W': False},
    '-': {'N': False, 'S': False, 'E': True, 'W': True},
    'L': {'N': True, 'S': False, 'E': True, 'W': False},
    'J': {'N': True, 'S': False, 'E': False, 'W': True},
    '7': {'N': False, 'S': True, 'E': False, 'W': True},
    'F': {'N': False, 'S': True, 'E': True, 'W': False},
    '.': {'N': False, 'S': False, 'E': False, 'W': False},
    'S': {'N': False, 'S': False, 'E': False, 'W': False}
  }
  checknorth, checksouth, checkeast, checkwest = True, True, True, True
  if (startingpos[0] == 0):
    checknorth = False
  if (startingpos[0] == (len(rawinputarray) - 1)):
    checksouth = False
  if (startingpos[1] == (len(rawinputarray[startingpos[0]]) - 1)):
    checkeast = False
  if (startingpos[1] == 0):
    checkwest = False
  north, south, east, west = False, False, False, False
  if checknorth:
    northchar = rawinputarray[startingpos[0] - 1][startingpos[1]]
    if pipes[northchar]['S']:
      north = True
  if checksouth:
    southchar = rawinputarray[startingpos[0] + 1][startingpos[1]]
    if pipes[southchar]['N']:
      south = True
  if checkeast:
    eastchar = rawinputarray[startingpos[0]][startingpos[1] + 1]
    if pipes[eastchar]['W']:
      east = True
  if checkwest:
    westchar = rawinputarray[startingpos[0]][startingpos[1] - 1]
    if pipes[westchar]['E']:
      west = True
  pipes['S']['N'] = north
  pipes['S']['S'] = south
  pipes['S']['E'] = east
  pipes['S']['W'] = west
  return pipes

def getnewdir(char, pipedict, prevdir):
  dirs = ['N', 'E', 'S', 'W']
  oppdir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E', '': ''}
  for dir in dirs:
    if (pipedict[char][dir] and (dir != oppdir[prevdir])):
      return dir

def increaseindir(currentloc, dir):
  newloc = currentloc
  if (dir == 'N'):
    newloc[0] -= 1
  elif (dir == 'S'):
    newloc[0] += 1
  elif (dir == 'E'):
    newloc[1] += 1
  elif (dir == 'W'):
    newloc[1] -= 1
  return newloc

def findpipeloop(startingpos, rawinputarray, pipedict):
  pipeloop = [startingpos]
  newdir = getnewdir('S', pipedict, '')
  newloc = startingpos
  newchar = ''
  while (newchar != 'S'):
    newloc = increaseindir(newloc, newdir)
    newchar = rawinputarray[newloc[0]][newloc[1]]
    newdir = getnewdir(newchar, pipedict, newdir)
    pipeloop.append(newloc.copy())
  return pipeloop

def sortbycol(pipeloop):
  return pipeloop[1]

def sortbyrow(pipeloop):
  return pipeloop[0]

def formatpipeloop(pipeloop):
  pipeloop.pop()
  pipeloop.sort(key=sortbycol)
  pipeloop.sort(key=sortbyrow)
  return pipeloop

def getcolsonly(pipeloop, endrow):
  newpipeloop = []
  for row in range(endrow):
    rowgroup = []
    for pipe in pipeloop:
      if (pipe[0] == row):
        rowgroup.append(pipe[1])
    newpipeloop.append(rowgroup)
  return newpipeloop

def checkS(pipedict):
  corners = ['F', '7', 'L', 'J']
  for i in corners:
    if (pipedict.get('S') == pipedict.get(i)):
      return i
  return 0

# function below needs to be fixed
# supposed to determine whether or not a piece of the array is inside the loop or not (validity)
# don't know how to make it do that
def checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval=0):
  recentcorner = ''
  orig = rawinputarray[row][col - 1]
  totoggle = {'F': 'J', 'L': '7'}
  if (cornerSval != 0):
    totoggle['S'] = totoggle.get(cornerSval)
  if col in pipeloopcols[row]:
    valid = not valid
    if orig in totoggle:
      recentcorner = orig
  else:
    return valid, col
  while col in pipeloopcols[row]:
    curr = rawinputarray[row][col]
    if (curr == '|'):
      valid = not valid
    elif (curr == totoggle.get(recentcorner)):
      valid = not valid
    elif curr in totoggle:
      if (curr != recentcorner):
        recentcorner = curr
    print ("row:", row, "col:", col, "valid:", valid)
    col += 1
  print ("row:", row, "col:", col, "valid:", valid)
  print ()
  return valid, col

def isinloop(pipeloop, rawinputarray, pipedict):
  charlocsinloop = []
  startrow = pipeloop[0][0] + 1
  endrow = pipeloop[-1][0]
  pipeloopcols = getcolsonly(pipeloop, endrow)
  cornerSval = checkS(pipedict)
  for row in range(startrow, endrow):
    valid = True
    col = pipeloopcols[row][0] + 1
    valid, col = checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval)
    while (col < pipeloopcols[row][-1]):
      if col in pipeloopcols[row]:
        col += 1
        valid  = not valid
        valid, col = checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval)
      else:
        if valid:
          charlocsinloop.append([row, col])
        col += 1
  return charlocsinloop

def visualdisp(charlocsinloop, pipelooplocs, rawinputarray):
  newinputarray = []
  coltens = [' ']
  colones = [' ']
  for i in range(len(rawinputarray[0])):
    colones.append(str(i)[-1])
    if (i >= 10):
      coltens.append(str(i)[0])
    else:
      coltens.append(' ')
  newinputarray.append(coltens)
  newinputarray.append(colones)
  for i in range(len(rawinputarray)):
    row = [str(i)]
    for j in range(len(rawinputarray[i])):
      if [i, j] in charlocsinloop:
        row.append('*')
      elif [i, j] in pipelooplocs:
        orig = rawinputarray[i][j]
        vischange = {'F': '┌', '7': '┐', 'J': '┘', 'L': '└'}
        if vischange.get(orig) is None:
          row.append(orig)
        else:
          row.append(vischange.get(orig))
      else:
        row.append('.')
    newinputarray.append(row)
  for line in newinputarray:
    print (' '.join(line))
  print ()

def main():
  rawinputarray = getinput()
  startingpos = findstartingpos(rawinputarray)
  pipedict = findpipedict(startingpos, rawinputarray)
  pipeloop = findpipeloop(startingpos, rawinputarray, pipedict)
  pipeloop = formatpipeloop(pipeloop)
  charlocsinloop = isinloop(pipeloop, rawinputarray, pipedict)
  visualdisp(charlocsinloop, pipeloop, rawinputarray)
  print (len(charlocsinloop))

main()
