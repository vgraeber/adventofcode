from pathlib import Path
import math

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def sortcubes(cubes):
  colors = ["red", "green", "blue"]
  allcubedata = []
  colorsonly = []
  for i in cubes:
    diced = i.split(' ')
    allcubedata.append(diced)
    colorsonly.append(diced[1])
  colorindexes = []
  for i in colors:
    try:
      colorindexes.append(colorsonly.index(i))
    except ValueError:
      colorindexes.append(-1)
  for i in colors:
    try:
      colorsonly.pop(colorsonly.index(i))
    except ValueError:
      pass
  newcubedata = []
  for i in range(len(colorindexes)):
    if (colorindexes[i] == -1):
      newcubedata.insert(i, 0)
    else:
      newcubedata.insert(i, int(allcubedata[colorindexes[i]][0]))
  return newcubedata

def sortgameinfo(rawinputlist):
  allgameinfo = []
  for i in rawinputlist:
    singlegameinfo = []
    game = i.split(':')
    gameid = int(game[0].split(' ')[1])
    gamesets = game[1].split(';')
    for j in gamesets:
      cubes = j.strip().split(", ")
      cubes = sortcubes(cubes)
      singlegameinfo.append(cubes)
    allgameinfo.append([gameid, singlegameinfo])
  return allgameinfo

def determineminimumcubes(cleaninputlist):
  minimumcubes = []
  for game in cleaninputlist:
    limit = [0, 0, 0]
    for gameset in game[1]:
      for i in range(len(gameset)):
        if (gameset[i] >  limit[i]):
          limit[i] = gameset[i]
    minimumcubes.append(limit)
  return minimumcubes

def getpowersofcubes(minimumcubes):
  powersofcubes = []
  for i in minimumcubes:
    powersofcubes.append(math.prod(i))
  return powersofcubes

def main():
  rawinputlist = getinput()
  cleaninputlist = sortgameinfo(rawinputlist)
  minimumcubes = determineminimumcubes(cleaninputlist)
  powersofcubes = getpowersofcubes(minimumcubes)
  print(sum(powersofcubes))

main()
