from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [list(line) for line in rawinputlist]
  return rawinputarray

def tiltplatform(arr, dir):
  rowdirs = {'N': [1, len(arr), 1], 'S': [(len(arr) - 2), -1, -1], 'E': [0, len(arr), 1], 'W': [0, len(arr), 1]}
  coldirs = {'N': [0, len(arr[0]), 1], 'S': [0, len(arr[0]), 1], 'E': [1, len(arr[0]), 1], 'W': [(len(arr[0]) - 2), -1, -1]}
  posdiff = {'N': [-1, 0], 'S': [1, 0], 'E': [0, -1], 'W': [0, 1]}
  bounds = {'N': ["UL", 0], 'S': ["LR", (len(arr) - 1)], 'E': ["UL", 0], 'W': ["LR", (len(arr[0]) - 1)]}
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
  cyc = ['N', 'W', 'S', 'E']
  numcycs = 3 #1000000000
  for i in range(numcycs):
    for dir in cyc:
      rawinputarray = tiltplatform(rawinputarray, dir)
    print (i)
    printarr(rawinputarray)
  load = calcload(rawinputarray)
  print (load)

main()
