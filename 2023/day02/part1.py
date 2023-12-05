from pathlib import Path

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

def removeinvalidgames(cleaninputlist):
  limit = [12, 13, 14]
  validgameids = []
  for game in cleaninputlist:
    validgame = True
    for gameset in game[1]:
      for i in range(len(limit)):
        if (gameset[i] >  limit[i]):
          validgame = False
    if (validgame):
      validgameids.append(game[0])
  return validgameids

def main():
  rawinputlist = getinput()
  cleaninputlist = sortgameinfo(rawinputlist)
  validgameids = removeinvalidgames(cleaninputlist)
  print(sum(validgameids))

main()
