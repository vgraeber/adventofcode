from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputlist = [line.split() for line in rawinputlist]
  rawinputlist = [[line[0], line[1].split(',')] for line in rawinputlist]
  return rawinputlist

def formatinputlist(rawinputlist):
  formattedinputlist = []
  for line in rawinputlist:
    springlist = list(line[0])
    brokenspringnums = []
    for i in line[1]:
      brokenspringnums.append(int(i))
    formattedinputlist.append([springlist, brokenspringnums])
  return formattedinputlist

def main():
  rawinputlist = getinput()
  formattedinputlist = formatinputlist(rawinputlist)
  print (formattedinputlist)

main()
