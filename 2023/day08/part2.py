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

def findstepstoexitandloop(currentmap, dirs, maps):
  stepinfo = []
  steps = 0
  while (len(stepinfo) < 2):
    for dir in dirs:
      currentmap = getmap(currentmap[dir], maps)
      steps += 1
    if checkmapsendinginletter('Z', [currentmap]):
      stepinfo.append(steps)
  return stepinfo

def getstepsneeded(dirs, maps):
  currentmaps = getmapsendinginletter('A', maps)
  allstepinfo = []
  for map in currentmaps:
    stepinfo = findstepstoexitandloop(map, dirs, maps)
    allstepinfo.append(stepinfo)
  allstepinfo.sort()
  print (allstepinfo)
  indesert = True
  while indesert:
    for ghost in range(len(allstepinfo) - 1):
      while (allstepinfo[ghost][0] < allstepinfo[ghost + 1][0]):
        allstepinfo[ghost][0] += allstepinfo[ghost][1]
        allstepinfo.sort()
    currentsteps = []
    for ghost in allstepinfo:
      currentsteps.append(ghost[0])
    if (currentsteps == ([currentsteps[0]] * len(currentsteps))):
      indesert = False
    else:
      print (currentsteps)
  return currentsteps

def main():
  dirs, maps = getinput()
  maps = formatmaps(maps)
  steps = getstepsneeded(dirs, maps)
  print ("steps needed:", steps)

main()
