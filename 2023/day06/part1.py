from pathlib import Path
import math

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def sortinput(rawinputlist):
  lessrawinput = []
  for i in rawinputlist:
    info = i.split()
    info.pop(0)
    lessrawinput.append(info)
  sortedinput = []
  for line in range(len(lessrawinput) // 2):
    for i in range(len(lessrawinput[line])):
      sortedinput.append([int(lessrawinput[0][i]), int(lessrawinput[1][i])])
  return sortedinput

def calcraceoptions(sortedinput):
  raceoptions = []
  for race in sortedinput:
    choices = []
    for i in range(race[0] + 1):
      hold = i
      dist = (race[0] - hold) * hold
      if (dist > race[1]):
        choices.append(i)
    raceoptions.append(len(choices))
  return raceoptions

def main():
  rawinputlist = getinput()
  sortedinput = sortinput(rawinputlist)
  raceoptions = calcraceoptions(sortedinput)
  print(math.prod(raceoptions))

main()
