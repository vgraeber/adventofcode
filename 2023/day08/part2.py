from pathlib import Path

def getinput():
  path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n\n")
  dirs = rawinputlist[0]
  maps = rawinputlist[1].split("\n")
  maps.pop()
  return dirs, maps

def formatmaps(maps):
  newmaps = []
  for map in maps:
    newmap = {}
    info = map.split(" = ")
    newmap["source"] = info[0]
    dirs = info[1].strip("()").split(", ")
    newmap['L'] = dirs[0]
    newmap['R'] = dirs[1]
    newmaps.append(newmap)
  return newmaps

def getmap(mapname, maps):
  for map in maps:
    if (map["source"] == mapname):
      return map

def getmapsendinginletter(letter, maps):
  mapsendinginletter = []
  for map in maps:
    if (map["source"][-1] == letter):
      mapsendinginletter.append(map)
  return mapsendinginletter

def checkmapsendinginletter(letter, maps):
  for map in maps:
    if (map["source"][-1] != letter):
      return False
  return True

def followdirs(dirs, maps):
  currentmaps = getmapsendinginletter('A', maps)
  steps = 0
  while not checkmapsendinginletter('Z', currentmaps):
    for dir in dirs:
      for map in range(len(currentmaps)):
        currentmaps[map] = getmap(currentmaps[map][dir], maps)
      steps += 1
  return steps

def main():
  dirs, maps = getinput()
  maps = formatmaps(maps)
  steps = followdirs(dirs, maps)
  print ("steps needed:", steps)

main()
