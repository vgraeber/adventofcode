from pathlib import Path

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
    info = ''.join(info)
    lessrawinput.append(info)
  sortedinput = []
  for i in range(len(lessrawinput)):
    sortedinput.append(int(lessrawinput[i]))
  print (sortedinput)
  return sortedinput

def calcraceoptions(sortedinput):
  raceoptions = 0
  for i in range(sortedinput[0] + 1):
    hold = i
    dist = (sortedinput[0] - hold) * hold
    if (dist > sortedinput[1]):
      raceoptions += 1
  return raceoptions

def main():
  rawinputlist = getinput()
  sortedinput = sortinput(rawinputlist)
  raceoptions = calcraceoptions(sortedinput)
  print(raceoptions)

main()
