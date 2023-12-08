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

def followdirs(dirs, maps):
  currentmap = getmap("AAA", maps)
  destmap = getmap("ZZZ", maps)
  steps = 0
  while (currentmap != destmap):
    for dir in dirs:
      currentmap = getmap(currentmap[dir], maps)
      steps += 1
  return steps

def main():
  dirs, maps = getinput()
  maps = formatmaps(maps)
  steps = followdirs(dirs, maps)
  print ("steps needed:", steps)

main()
