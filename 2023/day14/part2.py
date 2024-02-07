from pathlib import Path
import copy

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  return rawinputarray

def tiltplatform(arr, dir):
  rowdirs = {'N': [1, len(arr), 1], 'S': [(len(arr) - 2), -1, -1], 'W': [0, len(arr), 1], 'E': [0, len(arr), 1]}
  coldirs = {'N': [0, len(arr[0]), 1], 'S': [0, len(arr[0]), 1], 'W': [1, len(arr[0]), 1], 'E': [(len(arr[0]) - 2), -1, -1]}
  posdiff = {'N': [-1, 0], 'S': [1, 0], 'W': [0, -1], 'E': [0, 1]}
  bounds = {'N': ["UL", 0], 'S': ["LR", (len(arr) - 1)], 'W': ["UL", 0], 'E': ["LR", (len(arr[0]) - 1)]}
  for row in range(rowdirs[dir][0], rowdirs[dir][1], rowdirs[dir][2]):
    for col in range(coldirs[dir][0], coldirs[dir][1], coldirs[dir][2]):
      currchar = arr[row][col]
      newchar = arr[row + posdiff[dir][0]][col + posdiff[dir][1]]
      if (currchar != 'O'):
        continue
      elif (newchar != '.'):
        continue
      spacediff = 1
      while (newchar == '.'):
        spacediff += 1
        newrow = row + (spacediff * posdiff[dir][0])
        newcol = col + (spacediff * posdiff[dir][1])
        if (bounds[dir][0] == "UL"):
          if ((newrow < bounds[dir][1]) or (newcol < bounds[dir][1])):
            break
        elif (bounds[dir][0] == "LR"):
          if ((newrow > bounds[dir][1]) or (newcol > bounds[dir][1])):
            break
        newchar = arr[newrow][newcol]
      spacediff -= 1
      newrow = row + (spacediff * posdiff[dir][0])
      newcol = col + (spacediff * posdiff[dir][1])
      arr[newrow][newcol] = currchar
      arr[row][col] = '.'
  return arr

def getloopvals(arr, numcycs):
  cyc = ['N', 'W', 'S', 'E']
  prevarrs = [copy.deepcopy(arr)]
  for i in range(numcycs):
    for dir in cyc:
      arr = tiltplatform(arr, dir)
    prevarrs.append(copy.deepcopy(arr))
    for j in range(len(prevarrs) - 1):
      if (prevarrs[j] == arr):
        return ([j, ((i + 1) - j)], prevarrs[j:(i + 1)])

def calcload(arr):
  load = 0
  for row in range(len(arr)):
    for col in range(len(arr[row])):
      if (arr[row][col] == 'O'):
        load += len(arr) - row
  return load

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += col
    toprint += "\n"
  print (toprint)

def main():
  rawinputarray = getinput()
  numcycs = 1000000000
  loopnums, looparrs = getloopvals(rawinputarray, numcycs)
  endloopnum = (numcycs - loopnums[0]) % loopnums[1]
  load = calcload(looparrs[endloopnum])
  print (load)

main()
