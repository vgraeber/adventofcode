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

def changenumericwordstodigits(rawinputlist):
  numericwordsasdigits = {"zero": '0', "one": '1', "two": '2', "three": '3', "four": '4', "five": '5', "six": '6', "seven": '7', "eight": '8', "nine": '9'}
  pattern = re.compile(r"(?=(" + '|'.join(numericwordsasdigits.keys()) + r"))")
  lessrawinputlist = []
  for i in rawinputlist:
    lessrawinput = re.sub(pattern, lambda x: numericwordsasdigits.get(x.group(1)), i)
    lessrawinputlist.append(lessrawinput)
  return lessrawinputlist

def getdigitsonly(lessrawinputlist):
  cleaninputlist = []
  for i in lessrawinputlist:
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
  lessrawinputlist = changenumericwordstodigits(rawinputlist)
  cleaninputlist = getdigitsonly(lessrawinputlist)
  calibrationvalueslist = findcalibrationvalues(cleaninputlist)
  print(sumcalibrationvalues(calibrationvalueslist))

main()
