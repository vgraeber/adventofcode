from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  rawinputlist = [line.split() for line in rawinputlist]
  rawinputlist = [[line[0], line[1].split(',')] for line in rawinputlist]
  return rawinputlist

def splitbytype(line):
  prev = ''
  newline = []
  newgroup = ""
  for char in line:
    if (char != prev):
      newline.append(newgroup)
      prev = char
      newgroup = ''
    newgroup += char
  newline.append(newgroup)
  newline.pop(0)
  return newline

def formatinputlist(rawinputlist):
  formattedinputlist = []
  for line in rawinputlist:
    springlist = splitbytype(line[0])
    brokenspringnums = []
    for i in line[1]:
      brokenspringnums.append(int(i))
    formattedinputlist.append([springlist, brokenspringnums])
  return formattedinputlist

def condenselist(formattedinputlist):
  condensedlist = []
  for line in formattedinputlist:
    condensedline = []
    for i in range(len(line[0])):
      if (i != 0):
        prevchar = line[0][i - 1][0]
      else:
        prevchar = '.'
      if (i != (len(line[0]) - 1)):
        nextchar = line[0][i + 1][0]
      else:
        nextchar = '.'
      char = line[0][i][0]
      des = prevchar + char + nextchar
      if (char != '.'):
        condensedline.append([i, len(line[0][i]), des, None])
    condensedlist.append([condensedline, [[line[1][i], False] for i in range(len(line[1]))]])
  return condensedlist

def getminchars(nums):
  min = 0
  for num in nums:
    if not num[1]:
      min += num[0]
      min += 1
  min -= 1
  return min

def assigndefinite(condensedlist):
  line = 0
  while (line < len(condensedlist)):
    repeat = False
    springconditions = condensedlist[line][0]
    numsprings = condensedlist[line][1]
    scleft = 0
    nsleft = 0
    while (springconditions[scleft][2] == ".#."):
      if springconditions[scleft][3] is None:
        repeat = True
      else:
        scleft += 1
        nsleft += 1
        break
      condensedlist[line][0][scleft][3] = nsleft
      condensedlist[line][1][nsleft][1] = True
      scleft += 1
      nsleft += 1
    while (springconditions[scleft][2] == ".#?"):
      if springconditions[scleft][3] is None:
        repeat = True
      else:
        scleft += 1
        nsleft += 1
        break
      num = condensedlist[line][1][nsleft][0]
      currnum = springconditions[scleft][1]
      i = 1
      while (currnum < num):
        nextnum = springconditions[scleft + i][1]
        currnum += nextnum
        i += 1
      i -= 1
      endind = springconditions[scleft + i][0]
      popind = scleft + 1
      while (springconditions[popind][0] < endind):
        condensedlist[line][0].pop(popind)
      if (num == 1):
        condensedlist[line][0][scleft + 1][2] = condensedlist[line][0][scleft + 1][2][0] + '.' + condensedlist[line][0][scleft + 1][2][2]
      elif ((springconditions[scleft][0] + 1) == springconditions[scleft + 1][0]):
        condensedlist[line][0][scleft + 1][1] -= 1
      if (springconditions[scleft + 1][2] == "#.#"):
        condensedlist[line][0].pop(scleft + 1)
      diff = num - currnum
      condensedlist[line][0][scleft][1] = num
      condensedlist[line][0][scleft][2] = ".#."
      condensedlist[line][0][scleft][3] = nsleft
      if (i > 1):
        condensedlist[line][0][scleft + 1][1] = diff
      condensedlist[line][0][scleft + 1][2] = '.' + condensedlist[line][0][scleft + 1][2][1:]
      condensedlist[line][1][nsleft][1] = True
      scleft += 1
      nsleft += 1
    while (springconditions[scleft][2] == ".?#"):
      if springconditions[scleft][3] is None:
        repeat = True
      else:
        scleft += 1
        nsleft += 1
        break
      num = condensedlist[line][1][nsleft][0]
      currnum = springconditions[scleft + 1][1]
      if (currnum < num):
        thisnum = springconditions[scleft][1]
        currnum += thisnum
      i = 1
      while (currnum < num):
        nextnum = springconditions[scleft + i][1]
        currnum += nextnum
        i += 1
      i -= 1
      condensedlist[line][0].pop(scleft)
      endind = springconditions[scleft + i][0]
      popind = scleft + 1
      while (springconditions[popind][0] < endind):
        condensedlist[line][0].pop(popind)
      if (num == 1):
        condensedlist[line][0][scleft + 1][2] = condensedlist[line][0][scleft + 1][2][0] + '.' + condensedlist[line][0][scleft + 1][2][2]
      elif ((springconditions[scleft][0] + 1) == springconditions[scleft + 1][0]):
        condensedlist[line][0][scleft + 1][1] -= 1
      if (springconditions[scleft + 1][2] == "#.#"):
        condensedlist[line][0].pop(scleft + 1)
      diff = num - currnum
      condensedlist[line][0][scleft][1] = num
      condensedlist[line][0][scleft][2] = ".#."
      condensedlist[line][0][scleft][3] = nsleft
      if (i > 1):
        condensedlist[line][0][scleft + 1][1] = diff
      condensedlist[line][0][scleft + 1][2] = '.' + condensedlist[line][0][scleft + 1][2][1:]
      condensedlist[line][1][nsleft][1] = True
      scleft += 1
      nsleft += 1
    scright = len(springconditions) - 1
    nsright = len(numsprings) - 1
    while (springconditions[scright][2] == ".#."):
      if springconditions[scright][3] is None:
        repeat = True
      else:
        scright -= 1
        nsright -= 1
        break
      condensedlist[line][0][scright][3] = nsright
      condensedlist[line][1][nsright][1] = True
      scright -= 1
      nsright -= 1
    while (springconditions[scright][2] == "?#."):
      if springconditions[scright][3] is None:
        repeat = True
      else:
        scright -= 1
        nsright -= 1
        break
      num = condensedlist[line][1][nsright][0]
      currnum = springconditions[scright][1]
      i = 1
      while (currnum < num):
        nextnum = springconditions[scright - i][1]
        currnum += nextnum
        i += 1
      i -= 1
      popind = scright - i
      endind = springconditions[scright][0]
      while (springconditions[popind][0] < endind):
        condensedlist[line][0].pop(popind)
        scright -= 1
      if (num == 1):
        condensedlist[line][0][scright - 1][2] = condensedlist[line][0][scright - 1][2][0] + '.' + condensedlist[line][0][scright - 1][2][2]
      elif ((springconditions[scright][0] - 1) == springconditions[scright - 1][0]):
        condensedlist[line][0][scright - 1][1] -= 1
      if (springconditions[scright - 1][2] == "#.#"):
        condensedlist[line][0].pop(scright - 1)
        scright -= 1
      diff = num - currnum
      scright = popind
      condensedlist[line][0][scright][1] = num
      condensedlist[line][0][scright][2] = ".#."
      condensedlist[line][0][scright][3] = nsright
      if (i > 1):
        condensedlist[line][0][scright - 1][1] = diff
      condensedlist[line][0][scright - 1][2] = condensedlist[line][0][scright - 1][2][:2] + '.'
      condensedlist[line][1][nsright][1] = True
      scright -= 1
      nsright -= 1
    while (springconditions[scright][2] == "#?."):
      if springconditions[scright][3] is None:
        repeat = True
      else:
        scright -= 1
        nsright -= 1
        break
      num = condensedlist[line][1][nsright][0]
      currnum = springconditions[scright - 1][1]
      if (currnum < num):
        thisnum = springconditions[scright][1]
        currnum += thisnum
      i = 1
      while (currnum < num):
        nextnum = springconditions[scright - i][1]
        currnum += nextnum
        i += 1
      i -= 1
      condensedlist[line][0].pop(scright)
      scright -= 1
      popind = scright - i
      endind = springconditions[scright][0]
      while (springconditions[popind][0] < endind):
        condensedlist[line][0].pop(popind)
        scright -= 1
      if (num == 1):
        condensedlist[line][0][scright - 1][2] = condensedlist[line][0][scright - 1][2][0] + '.' + condensedlist[line][0][scright - 1][2][2]
      elif ((springconditions[scright][0] - 1) == springconditions[scright - 1][0]):
        condensedlist[line][0][scright - 1][1] -= 1
      if (springconditions[scright - 1][2] == "#.#"):
        condensedlist[line][0].pop(scright - 1)
        scright -= 1
      diff = num - currnum
      condensedlist[line][0][scright][1] = num
      condensedlist[line][0][scright][2] = ".#."
      condensedlist[line][0][scright][3] = nsright
      if (i > 1):
        condensedlist[line][0][scright - 1][1] = diff
      condensedlist[line][0][scright - 1][2] = condensedlist[line][0][scright - 1][2][:2] + '.'
      condensedlist[line][1][nsright][1] = True
      scright -= 1
      nsright -= 1
    check = 0
    while (check < len(springconditions)):
      if (springconditions[check][1] == 0):
        springconditions.pop(check)
      else:
        check += 1
    if not repeat:
      line += 1
  for i in range(len(condensedlist)):
    mins = getminchars(condensedlist[i][1])
    numnones = 0
    for j in condensedlist[i][0]:
      if j[3] is None:
        numnones += 1
    if ((numnones == 1) and (condensedlist[i][0][0][1] == mins)):
      newline = []
      startind = condensedlist[i][0][0][0]
      for num in range(len(condensedlist[i][1])):
        newline.append([startind, condensedlist[i][1][num], ".#.", num])
        startind += condensedlist[i][1][num][0] + 1
        condensedlist[i][1][num][1] = True
      condensedlist[i][0] = newline
  return condensedlist

def remdefinite(condensedlist):
  trimmedlist = []
  for line in condensedlist:
    newgroup = []
    newnums = []
    for group in line[0]:
      if group[3] is None:
        newgroup.append(group)
    for nums in line[1]:
      if not nums[1]:
        newnums.append(nums)
    trimmedlist.append([newgroup, newnums])
  return trimmedlist

def calcnumarrangements(trimmedlist):
  numarrangements = []
  for line in trimmedlist:
    if (len(line[1]) == 0):
      numarrangements.append(1)
    else:
      mins = []
      for i in range(len(line[1])):
        minnum = getminchars(line[1][:(i + 1)])
        mins.append(minnum)
      buffers = len(line[1]) - 1
      for i in range(len(line[0])):
        if (line[0][i][1] >= mins[0]):
          print ("wrong code; fix later")
      numarrangements.append("wip")
  return numarrangements

def main():
  rawinputlist = getinput()
  formattedinputlist = formatinputlist(rawinputlist)
  condensedlist = condenselist(formattedinputlist)
  condensedlist = assigndefinite(condensedlist)
  trimmedlist = remdefinite(condensedlist)
  for line in trimmedlist:
    print (line)
  numarrangements = calcnumarrangements(trimmedlist)
  print (numarrangements)

main()
