from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input2.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  if (rawinputlist[-1] == ''):
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
  newloc = currentloc.copy()
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
  pipeloop = []
  newloc = startingpos.copy()
  newchar = ''
  newdir = getnewdir('S', pipedict, '')
  pipeloop.append(newloc.copy())
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
  if (pipedict.get('S') == pipedict.get('|')):
    return '|'
  return None

def checkcorners(valid, row, col, othercorners, rawinputarray):
  othercorner = None
  while othercorner is None:
    curr = rawinputarray[row][col]
    othercorner = othercorners.get(curr)
    col += 1
  if othercorner:
    valid = not valid
  return valid, col

def checkverts(valid, row, col, rawinputarray):
  verts = 0
  while ((col < len(rawinputarray[row])) and (rawinputarray[row][col] == '|')):
    verts += 1
    col += 1
  if ((verts % 2) != 0):
    valid = not valid
  return valid, col

# function below needs to be fixed
# supposed to determine whether or not a piece of the array is inside the loop or not (validity)
# don't know how to make it do that
def checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval):
  totoggle = {'F': {'J': True, '7': False}, 'L': {'7': True, 'J': False}}
  vertS = False
  if cornerSval is not None:
    initcorners = ['F', 'L']
    endcorners = ['J', '7']
    if cornerSval in initcorners:
      totoggle['S'] = totoggle.get(cornerSval)
    elif cornerSval in endcorners:
      totoggle['F']['S'] = totoggle.get('F').get(cornerSval)
      totoggle['L']['S'] = totoggle.get('L').get(cornerSval)
    else:
      vertS = True
  while col in pipeloopcols[row]:
    curr = rawinputarray[row][col]
    if (curr in totoggle):
      othercorners = totoggle.get(curr)
      valid, col = checkcorners(valid, row, col, othercorners, rawinputarray)
    elif ((curr == '|') or ((curr == 'S') and vertS)):
      valid, col = checkverts(valid, row, col, rawinputarray)
      vertS = False
  return valid, col

def isinloop(pipeloop, rawinputarray, pipedict):
  charlocsinloop = []
  startrow = pipeloop[0][0] + 1
  endrow = pipeloop[-1][0]
  pipeloopcols = getcolsonly(pipeloop, endrow)
  cornerSval = checkS(pipedict)
  for row in range(startrow, endrow):
    valid = False
    col = pipeloopcols[row][0]
    valid, col = checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval)
    while (col < pipeloopcols[row][-1]):
      if col in pipeloopcols[row]:
        valid, col = checktoggles(valid, row, col, pipeloopcols, rawinputarray, cornerSval)
      else:
        if valid:
          charlocsinloop.append([row, col])
        col += 1
  return charlocsinloop

def visualdisp(charlocsinloop, pipelooplocs, rawinputarray):
  newinputarray = []
  buffer = ''
  colhundreds = ['   ', buffer]
  coltens = ['   ', buffer]
  colones = ['   ', buffer]
  for i in range(len(rawinputarray[0])):
    num = str(i)
    if (len(num) < 3):
      diff = 3 - len(num)
      num = ('0' * diff) + num
    colones.append(num[2])
    if (i >= 10):
      coltens.append(num[1])
    else:
      coltens.append(' ')
    if (i >= 100):
      colhundreds.append(num[0])
    else:
      colhundreds.append(' ')
  newinputarray.append(colhundreds)
  newinputarray.append(coltens)
  newinputarray.append(colones)
  for i in range(len(rawinputarray)):
    num = str(i)
    if (len(num) < 3):
      diff = 3 - len(num)
      num = ('0' * diff) + num
    row = [num]
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
    print (buffer.join(line))
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
