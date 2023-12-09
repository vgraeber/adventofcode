from pathlib import Path

def getinput():
  path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def getsortedinput(rawinputlist):
  sortedinputlist = []
  for line in rawinputlist:
    vals = [int(i) for i in line.split()]
    sortedinputlist.append(vals)
  return sortedinputlist

def getprediction(hist):
  diffinhist = []
  for num in range(len(hist) - 1):
    diff = hist[num + 1] - hist[num]
    diffinhist.append(diff)
  return diffinhist

def checkpredictlist(predictlist):
  tocheck = predictlist[-1]
  if (tocheck != ([0] * len(tocheck))):
    return False
  return True

def getpredictions(hist):
  predictlist = [hist]
  while not checkpredictlist(predictlist):
    newpredict = getprediction(predictlist[-1])
    predictlist.append(newpredict)
  return predictlist

def makepredictions(hist):
  for predict in range((len(hist) - 1), 0, -1):
    predictval = hist[predict - 1][0] - hist[predict][0]
    hist[predict - 1].insert(0, predictval)
  return hist

def getexpovals(sortedinputlist):
  for hist in range(len(sortedinputlist)):
    sortedinputlist[hist] = getpredictions(sortedinputlist[hist])
  for hist in range(len(sortedinputlist)):
    sortedinputlist[hist] = makepredictions(sortedinputlist[hist])
  return sortedinputlist

def getexpovalsonly(expoinputlist):
  expovalslist = []
  for hist in expoinputlist:
    expovalslist.append(hist[0][0])
  return expovalslist

def main():
  rawinputlist = getinput()
  sortedinputlist = getsortedinput(rawinputlist)
  expoinputlist = getexpovals(sortedinputlist)
  expovalslist = getexpovalsonly(expoinputlist)
  print (sum(expovalslist))

main()
