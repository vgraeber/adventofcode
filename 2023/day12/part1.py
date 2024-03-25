from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputlist = [line.split() for line in rawinputlist]
  rawinputlist = [[line[0], [int(num) for num in line[1].split(',')]] for line in rawinputlist]
  return rawinputlist

def splitbytype(line):
  prev = ''
  newline = []
  newgroup = ""
  for char in line:
    if (char != prev):
      newline.append([prev, len(newgroup)])
      prev = char
      newgroup = ''
    newgroup += char
  newline.append([prev, len(newgroup)])
  newline.pop(0)
  return newline

def formatinput(rawinputlist):
  formattedinput = []
  for line in rawinputlist:
    newsprings = splitbytype(line[0])
    formattedinput.append([newsprings, line[1]])
  return formattedinput

def getquesmarks(line):
  num = 0
  for block in line:
    if (block[0] == '?'):
      num += 1
  return num

def findknowns(formattedinput):
  buffer = ['.', 1]
  for line in formattedinput:
    nqmkgrps = getquesmarks(line[0])
    if (nqmkgrps == 1):
      print (line, nqmkgrps)
    else:
      print (line, nqmkgrps)

def printarr(arr):
  toprint = ""
  for row in arr:
    toprint += str(row)
    toprint += "\n"
  print (toprint)

def main():
  rawinputlist = getinput()
  formattedinput = formatinput(rawinputlist)
  findknowns(formattedinput)

main()
