from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputarray = [line.split(' ') for line in rawinputlist]
  return rawinputarray

def printarr(arr):
  toprint = ""
  for row in arr:
    for col in row:
      toprint += col[0]
    toprint += "\n"
  print (toprint)

def convinput(arr):
  dirconv = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
  newarr = [[dirconv[line[2][-2]], int("0x" + line[2][2:-2], 0)] for line in arr]
  return newarr

def move(pos, dir, mult):
  moveindir = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
  pos[0] += moveindir[dir][0] * mult
  pos[1] += moveindir[dir][1] * mult
  return pos

def getcoords(inputarr):
  pos = [0, 0]
  coords = [pos.copy()]
  bord = 0
  for line in inputarr:
    pos = move(pos, line[0], int(line[1]))
    coords.append(pos.copy())
    bord += int(line[1])
  return coords, bord

def doshoelace(coords, bord):
  pos = 0
  neg = 0
  for i in range(len(coords) - 1):
    curr = coords[i]
    next = coords[i + 1]
    pos += curr[0] * next[1]
    neg += curr[1] * next[0]
  area = (1 / 2) * (abs(pos - neg) + bord) + 1
  return area

def main():
  rawinputarray = getinput()
  rawinputarray = convinput(rawinputarray)
  coords, bord = getcoords(rawinputarray)
  area = doshoelace(coords, bord)
  print (area)

main()
