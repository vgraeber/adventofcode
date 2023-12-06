from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
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
      if (len(words) == 1):
        newlinecontent = []
        temp = []
        for i in range(len(linecontent)):
          temp.append(int(linecontent[i]))
          if ((i % 2) == 1):
            newlinecontent.append(temp)
            temp = []
        categorycontent = newlinecontent
      else:
        categorycontent.append([int(i) for i in linecontent])
    sortedinputlist.append([categoryname, categorycontent])
  return sortedinputlist

def condensedata(seeddata, seedranges):
  remranges = []
  remdata = []
  seedranges.sort()
  if ((len(seeddata) != len(seedranges)) and (len(seedranges) > 1)):
    for i in range(len(seedranges)):
      for j in range(1, len(seedranges) - i):
        oldseed = seedranges[i]
        newseed = seedranges[i + j]
        if (oldseed == newseed):
          remranges.append(i + j)
        elif (oldseed[0] == newseed[0]):
          remranges.append(i + j)
          k = str(newseed[0]) + '-' + str(newseed[1] - newseed[0] + 1)
          remdata.append(k)
  newseedranges = []
  for i in range(len(seedranges)):
    if i not in remranges:
      newseedranges.append(seedranges[i])
  newseeddata = {}
  for k, v in seeddata.items():
    if k not in remdata:
      newseeddata[k] = v
  return newseeddata, newseedranges

def convseeds(seeds, toconv):
  newseeds = []
  for seedgroup in seeds:
    key = str(seedgroup[0]) + '-' + str(seedgroup[1])
    seeddata = {key: -1}
    seedranges = []
    for map in range(len(toconv)):
      mapstart = toconv[map][1]
      mapstop = (toconv[map][1] + toconv[map][2])
      seedstart = seedgroup[0]
      seedend = (seedgroup[0] + seedgroup[1] - 1)
      if ((mapstart <= seedstart) and (seedend < mapstop)):
        seeddata[key] = map
        seedranges.append([seedstart, seedend])
      elif ((seedstart < mapstart) and (mapstop <= seedend)):
        underdiff = mapstart - seedstart
        overdiff = seedend - mapstop + 1
        cover = toconv[map][2]
        seeddata.pop(key, "")
        key1 = str(seedstart) + '-' + str(underdiff)
        key2 = str(mapstart) + '-' + str(cover)
        key3 = str(mapstop) + '-' + str(overdiff)
        seeddata.setdefault(key1, -1)
        seeddata[key2] = map
        seeddata.setdefault(key3, -1)
        seedranges.append([seedstart, (seedstart + underdiff - 1)])
        seedranges.append([mapstart, (mapstart + cover - 1)])
        seedranges.append([mapstop, (mapstop + overdiff - 1)])
      elif (mapstart <= seedstart < mapstop):
        overdiff = seedend - mapstop + 1
        cover = mapstop - seedstart
        seeddata.pop(key, "")
        key1 = str(seedstart) + '-' + str(cover)
        key2 = str(mapstop) + '-' + str(overdiff)
        seeddata[key1] = map
        seeddata.setdefault(key2, -1)
        seedranges.append([seedstart, (seedstart + cover - 1)])
        seedranges.append([mapstop, (mapstop + overdiff - 1)])
      elif (mapstart <= seedend < mapstop):
        underdiff = mapstart - seedstart
        cover = seedend - mapstart + 1
        seeddata.pop(key, "")
        key1 = str(seedstart) + '-' + str(underdiff)
        key2 = str(mapstart) + '-' + str(cover)
        seeddata.setdefault(key1, -1)
        seeddata[key2] = map
        seedranges.append([seedstart, (seedstart + underdiff - 1)])
        seedranges.append([mapstart, (mapstart + cover - 1)])
      seeddata, seedranges = condensedata(seeddata, seedranges)
    if (seeddata.get(key) == -1):
      newseeds.append(seedgroup)
    elif seeddata.get(key) is not None:
      seed = [int(i) for i in key.split('-')]
      v = seeddata.get(key)
      diff = toconv[v][0] - toconv[v][1]
      newseeds.append([(seed[0] + diff), seed[1]])
    else:
      for k, v in seeddata.items():
        seed = [int(i) for i in k.split('-')]
        if (v == -1):
          newseeds.append(seed)
        else:
          diff = toconv[v][0] - toconv[v][1]
          newseeds.append([(seed[0] + diff), seed[1]])
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
        print ("Error, cannot convert further.")
      toconv = sortedinput[next][1]
      convdata = convseeds(convdata, toconv)
  return convdata

def locvalsonly(convdata):
  locvals = [i[0] for i in convdata]
  return locvals

def main():
  rawinputlist = getinput()
  sortedinputlist = sortinput(rawinputlist)
  convdata = convthrough(sortedinputlist)
  locvals = locvalsonly(convdata)
  print (min(locvals))

main()
