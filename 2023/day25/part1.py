from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  lessrawinputlist = [line.split(": ") for line in rawinputlist]
  filteredinputlist = [[line[0], line[1].split()] for line in lessrawinputlist]
  return filteredinputlist

def formatinput(inputlist):
  newinputlist = {}
  for line in inputlist:
    if (line[0] in newinputlist):
      for cnctn in line[1]:
        if (cnctn not in newinputlist[line[0]]):
          newinputlist[line[0]].append(cnctn)
        if (cnctn not in newinputlist):
          newinputlist[cnctn] = [line[0]]
        else:
          newinputlist[cnctn].append(line[0])
    else:
      newinputlist[line[0]] = line[1]
      for cnctn in line[1]:
        if (cnctn not in newinputlist):
          newinputlist[cnctn] = [line[0]]
        else:
          newinputlist[cnctn].append(line[0])
  return newinputlist

def printarr(arr):
  toprint = ""
  for row in arr.keys():
    toprint += row
    toprint += str(arr[row])
    toprint += "\n"
  print (toprint)

def main():
  inputlist = getinput()
  inputlist = formatinput(inputlist)
  printarr(inputlist)

main()
