import re
from pathlib import Path
import string

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def findsymbollocs(rawinputlist):
  symbols = string.punctuation.replace('.', '')
  symbollocs = []
  for line in range(len(rawinputlist)):
    for i in range(len(rawinputlist[line])):
      if rawinputlist[line][i] in symbols:
        symbollocs.append([line, i])
  return symbollocs

def isInt(num):
  try:
    int(num)
    return True
  except (ValueError, TypeError):
    return False

def getgoodadjacentlocs(rawinputlist, symbollocs):
  allgoodadjacentlocs = []
  for symbol in symbollocs:
    adjacentlocs = [[(symbol[0] - 1), (symbol[1] - 1)], [(symbol[0] - 1), symbol[1]], [(symbol[0] - 1), (symbol[1] + 1)], [symbol[0], (symbol[1] - 1)], [symbol[0], (symbol[1] + 1)], [(symbol[0] + 1), (symbol[1] - 1)], [(symbol[0] + 1), symbol[1]], [(symbol[0] + 1), (symbol[1] + 1)]]
    goodadjacentlocs = []
    for loc in range(len(adjacentlocs)):
      good = True
      for i in range(len(adjacentlocs[loc])):
        if ((adjacentlocs[loc][i] < 0) or (adjacentlocs[loc][i] > len(rawinputlist)) or (adjacentlocs[loc][i] > len(rawinputlist[adjacentlocs[loc][0]]))):
          good = False
        elif not isInt(rawinputlist[adjacentlocs[loc][0]][adjacentlocs[loc][1]]):
          good = False
      if good:
        goodadjacentlocs.append(adjacentlocs[loc])
    allgoodadjacentlocs.append(goodadjacentlocs)
  return allgoodadjacentlocs

def findnums(sortedgoodadjacentlocs, rawinputlist):
  numlocs = []
  for symbol in sortedgoodadjacentlocs:
    for loc in symbol:
      i = loc[1]
      while ((i >= 0) and isInt(rawinputlist[loc[0]][i])):
        i -= 1
      left = (i + 1)
      i = loc[1]
      while ((i < len(rawinputlist[loc[0]])) and isInt(rawinputlist[loc[0]][i])):
        i += 1
      right = (i - 1)
      if [loc[0], [left, right]] not in numlocs:
        numlocs.append([loc[0], [left, right]])
  return numlocs

def getnums(numlocs, rawinputlist):
  numlist = []
  for num in numlocs:
    num = rawinputlist[num[0]][num[1][0]:(num[1][1] + 1)]
    numlist.append(int(num))
  return numlist

def main():
  rawinputlist = getinput()
  symbollocs = findsymbollocs(rawinputlist)
  allgoodadjacentlocs = getgoodadjacentlocs(rawinputlist, symbollocs)
  numlocs = findnums(allgoodadjacentlocs, rawinputlist)
  numlist = getnums(numlocs, rawinputlist)
  print(sum(numlist))

main()
