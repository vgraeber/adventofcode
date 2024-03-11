from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  filteredinputlist = [list(line) for line in rawinputlist]
  return filteredinputlist

def getstartpos(inputlist):
  startpos = [0, 0]
  for line in range(len(inputlist)):
    for char in range(len(inputlist[line])):
      if (inputlist[line][char] == 'S'):
        startpos = [line, char]
  return startpos

def inbounds(newpos, inputlist):
  vertbounds = [0, len(inputlist)]
  horizbounds = [0, len(inputlist[0])]
  if ((vertbounds[0] <= newpos[0] < vertbounds[1]) and (horizbounds[0] <= newpos[1] < horizbounds[1])):
    return True
  return False

def cango(char):
  plotdict = {'S': True, '.': True, '#': False, 'O': True}
  return plotdict[char]

def dosteps(inputlist, startpos, numsteps):
  dirs = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
  currsteps = 0
  posqueue = [startpos.copy()]
  while (currsteps < numsteps):
    newposqueue = []
    for pos in posqueue:
      for dir in dirs.values():
        newpos = [pos[0] + dir[0], pos[1] + dir[1]]
        if (inbounds(newpos, inputlist) and cango(inputlist[newpos[0]][newpos[1]])):
          if (inputlist[newpos[0]][newpos[1]] != 'O'):
            inputlist[newpos[0]][newpos[1]] = 'O'
          if (inputlist[pos[0]][pos[1]] == 'O'):
            inputlist[pos[0]][pos[1]] = '.'
            if ([pos[0], pos[1]] == startpos):
              inputlist[pos[0]][pos[1]] = 'S'
          if (newpos not in newposqueue):
            newposqueue.append(newpos)
    currsteps += 1
    posqueue = newposqueue
#    print (currsteps)
#    printarr(inputlist)

def countplots(inputlist):
  numplots = 0
  for line in inputlist:
    for char in line:
      if (char == 'O'):
        numplots += 1
  return numplots

def printarr(arr):
  printstr = ""
  for line in arr:
    for char in line:
      printstr += char
    printstr += "\n"
  print (printstr)

def main():
  inputlist = getinput()
  startpos = getstartpos(inputlist)
  dosteps(inputlist, startpos, 64)
  print (countplots(inputlist))

main()
