import re
from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def getdigitsonly(rawinputlist):
  cleaninputlist = []
  for i in rawinputlist:
    cleaninput = re.sub("\D", '', i)
    cleaninputlist.append(cleaninput)
  return cleaninputlist

def findcalibrationvalues(cleaninputlist):
  calibrationvalueslist = []
  for i in cleaninputlist:
    calibrationvalue = int(i[0] + i[-1])
    calibrationvalueslist.append(calibrationvalue)
  return calibrationvalueslist

def sumcalibrationvalues(calibrationvalueslist):
  return sum(calibrationvalueslist)

def main():
  rawinputlist = getinput()
  cleaninputlist = getdigitsonly(rawinputlist)
  calibrationvalueslist = findcalibrationvalues(cleaninputlist)
  print(sumcalibrationvalues(calibrationvalueslist))

main()
