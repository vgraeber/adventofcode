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

def formatseeds(convdata):
  newconvdata = []
  for i in convdata:
    for j in range(i[1]):
      newconvdata.append(i[0] + j)
  return newconvdata

def convseed(seed, toconv):
  conv = -1
  for map in range(len(toconv)):
    if (toconv[map][1] <= seed < (toconv[map][1] + toconv[map][2])):
      conv = map
  if (conv == -1):
    return seed
  else:
    return (toconv[conv][0] + (seed - toconv[conv][1]))

def convthrough(sortedinput):
  convdata = []
  for category in range(len(sortedinput)):
    titles = sortedinput[category][0]
    data = sortedinput[category][1]
    if (titles[0] == "start"):
      convdata = data
      #convdata = formatseeds(convdata)
    else:
      next = -1
      for i in range(len(sortedinput)):
        if (sortedinput[i][0][1] == titles[1]):
          next = i
          break
      if (next == -1):
        print("Error, cannot convert further.")
      toconv = sortedinput[next][1]
      for seed in range(len(convdata)):
        convdata[seed] = convseed(convdata[seed], toconv)
  return convdata

def main():
  rawinputlist = getinput()
  sortedinputlist = sortinput(rawinputlist)
  convdata = convthrough(sortedinputlist)
  print(min(convdata))

main()
