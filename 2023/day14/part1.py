from pathlib import Path

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
  rowdirs = {'N': [1, len(arr), 1], 'S': [(len(arr) - 2), -1, -1], 'E': [0, len(arr), 1], 'W': [0, len(arr), 1]}
  coldirs = {'N': [0, len(arr[0]), 1], 'S': [0, len(arr[0]), 1], 'E': [1, len(arr[0]), 1], 'W': [(len(arr[0]) - 2), -1, -1]}
  posdiff = {'N': [-1, 0], 'S': [1, 0], 'E': [0, -1], 'W': [0, 1]}
  bounds = {'N': ["UL", 0], 'S': ["LR", len(arr)], 'E': ["UL", 0], 'W': ["LR", len(arr[0])]}
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
    charrow = ""
    for col in range(len(arr[row])):
      currchar = arr[row][col]
      charrow += currchar
      if (currchar == 'O'):
        load += len(arr) - row
    print (charrow, load)
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
  rawinputarray = tiltplatform(rawinputarray, 'N')
  load = calcload(rawinputarray)
  print (load)

main()
