from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n\n")
  return rawinputlist

def sortinput(rawinputlist):
  sortedinputlist = []
  for category in rawinputlist:
    lessrawinput = category.split(':')
    title = lessrawinput[0].split()[0]
    words = title.split('-')
    categoryname = ""
    if (len(words) == 1):
      categoryname = ["start", "seed"]
    else:
      categoryname = [words[0], words[2]]
    contents = lessrawinput[1].strip().split("\n")
    categorycontent = []
    for line in contents:
      linecontent = line.split()
      newlinecontent = []
      if (len(words) == 1):
        temp = []
        for i in range(len(linecontent)):
          temp.append(int(linecontent[i]))
          if ((i % 2) == 1):
            newlinecontent.append(temp)
            temp = []
        categorycontent = newlinecontent
      else:
        for i in range(len(linecontent)):
          newlinecontent.append(int(linecontent[i]))
        categorycontent.append(newlinecontent)
    sortedinputlist.append([categoryname, categorycontent])
  return sortedinputlist

def convseed(seed, mapstart, mapdest):
  diff = seed - mapstart
  return (mapdest + diff)

def convseeds(seeds, toconv):
  newseeds = []
  for seedgroup in seeds:
    key = str(seedgroup[0]) + '-' + str(seedgroup[1])
    seeddata = {key: -1}
    for map in range(len(toconv)):
      mapstart = toconv[map][1]
      mapstop = (toconv[map][1] + toconv[map][2])
      seedstart = seedgroup[0]
      seedend = (seedgroup[0] + (seedgroup[1] - 1))
      if ((mapstart <= seedstart) and (seedend < mapstop)):
        seeddata[key] = map
      elif (mapstart <= seedstart < mapstop):
        overdiff = seedend - mapstop
        cover = mapstop - seedstart
        seeddata.pop(key, "")
        key1 = str(seedstart) + '-' + str(cover)
        key2 = str(mapstop) + '-' + str(overdiff)
        seeddata[key1] = map
        seeddata.setdefault(key2, -1)
      elif (mapstart <= seedend < mapstop):
        underdiff = mapstart - seedstart
        cover = seedend - mapstart
        seeddata.pop(key, "")
        key1 = str(seedstart) + '-' + str(underdiff)
        key2 = str(mapstart) + '-' + str(cover)
        seeddata.setdefault(key1, -1)
        seeddata[key2] = map
    if (seeddata.get(key) == -1):
      newseeds.append(seedgroup)
    elif (seeddata.get(key) != None):
      v = seeddata.get(key)
      newseeds.append([convseed(seedstart, toconv[v][1], toconv[v][0]), seedgroup[1]])
    else:
      for k, v in seeddata.items():
        if (v == -1):
          seed = [int(i) for i in k.split('-')]
          newseeds.append(seed)
        else:
          seed = [int(i) for i in k.split('-')]
          newseeds.append([convseed(seed[0], toconv[v][1], toconv[v][0]), seed[1]])
  print(newseeds)
  return newseeds

def convthrough(sortedinput):
  convdata = []
  for category in range(len(sortedinput)):
    titles = sortedinput[category][0]
    data = sortedinput[category][1]
    if (titles[0] == "start"):
      convdata = data
    else:
      next = -1
      for i in range(len(sortedinput)):
        if (sortedinput[i][0][1] == titles[1]):
          next = i
          break
      if (next == -1):
        print("Error, cannot convert further.")
      toconv = sortedinput[next][1]
      convdata = convseeds(convdata, toconv)
  return convdata

def locvalsonly(convdata):
  locvals = []
  for i in convdata:
    locvals.append(i[0])
  return locvals

def main():
  rawinputlist = getinput()
  sortedinputlist = sortinput(rawinputlist)
  convdata = convthrough(sortedinputlist)
  locvals = locvalsonly(convdata)
  print(min(locvals))

main()
