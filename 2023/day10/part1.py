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
  pipeloop = ['S']
  newdir = getnewdir('S', pipedict, '')
  newloc = startingpos
  newchar = ''
  while (newchar != 'S'):
    newloc = increaseindir(newloc, newdir)
    newchar = rawinputarray[newloc[0]][newloc[1]]
    newdir = getnewdir(newchar, pipedict, newdir)
    pipeloop.append(newchar)
  return pipeloop

def main():
  rawinputarray = getinput()
  startingpos = findstartingpos(rawinputarray)
  pipedict = findpipedict(startingpos, rawinputarray)
  pipeloop = findpipeloop(startingpos, rawinputarray, pipedict)
  halfwaymark = len(pipeloop) // 2
  print (halfwaymark)

main()
