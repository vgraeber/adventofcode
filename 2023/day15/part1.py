from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinput = rawinput.replace("\n", '')
  rawinputarray = rawinput.split(',')
  return rawinputarray

def runhash(strinput):
  res = 0
  for charinput in strinput:
    res += ord(charinput)
    res *= 17
    res %= 256
  return res

def main():
  rawinputarray = getinput()
  tot = 0
  for strinput in rawinputarray:
    res = runhash(strinput)
    tot += res
  print (tot)

main()
