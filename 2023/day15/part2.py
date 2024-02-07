from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinput = rawinput.replace("\n", '')
  rawinput = rawinput.replace('=', " = ")
  rawinput = rawinput.replace('-', " -")
  rawinputlist = rawinput.split(',')
  rawinputarray = [line.split(' ') for line in rawinputlist]
  return rawinputarray

def runhash(strinput):
  strinput = ''.join(strinput)
  res = 0
  for charinput in strinput:
    res += ord(charinput)
    res *= 17
    res %= 256
  return str(res)

def runhashmap(boxnum, strinput, boxes):
  label = strinput[0]
  op = strinput[1]
  boxes.setdefault(boxnum, {})
  if (op == '-'):
    boxes[boxnum].pop(label, None)
  elif (op == '='):
    boxes[boxnum].update({label: strinput[2]})
  if (boxes[boxnum] == {}):
    boxes.pop(boxnum)
  return boxes

def getfocusingpower(boxnum, boxvals):
  power = 0
  i = 1
  for val in boxvals.values():
    power += (boxnum + 1) * i * int(val)
    i += 1
  return power

def main():
  rawinputarray = getinput()
  hasharr = []
  for strinput in rawinputarray:
    hasharr.append(runhash(strinput[0]))
  boxes = {}
  for i in range(len(rawinputarray)):
    runhashmap(hasharr[i], rawinputarray[i], boxes)
  focusingpower = []
  for boxnum, boxvals in boxes.items():
    focusingpower.append(getfocusingpower(int(boxnum), boxvals))
  print (sum(focusingpower))

main()
