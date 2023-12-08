from pathlib import Path

def getinput():
  path = Path(__file__).parent / "input2.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def sorthand(card):
  ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
  return ranks.index(card)

def gethandtype(hvals):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  type = 6
  if (len(hvals) == 1):
    type = 0
  elif (hvals[0] == 4):
    type = 1
  elif (hvals[0] == 3):
    if (hvals[1] == 2):
      type = 2
    else:
      type = 3
  elif (hvals[0] == 2):
    if (hvals[1] == 2):
      type = 4
    else:
      type = 5
  return types[type]

def sorthdicts(hdict):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  return types.index(hdict[1])

def sortcardinfo(rawinputlist):
  sortedinputlist = []
  for line in rawinputlist:
    lessrawinfo = line.split()
    hand = list(lessrawinfo[0])
    hand.sort(key=sorthand)
    hdict = {}
    for card in hand:
      if card in hdict:
        hdict[card] += 1
      else:
        hdict[card] = 1
    hvals = list(hdict.values())
    hvals.sort(reverse=True)
    type = gethandtype(hvals)
    rank = 0
    bid = int(lessrawinfo[1])
    sortedinputlist.append([list(lessrawinfo[0]), type, rank, bid])
  sortedinputlist.sort(key=sorthdicts)
  return sortedinputlist

def sortsecondindex(l):
  return l[1]

def repeatscheck(inputlist, log=False):
  temp = []
  for i in inputlist:
    if i[1] in temp:
      if log:
        print ("input:", inputlist)
        print ("temp:", temp)
        print ("i:", i)
        print ()
      return False
    else:
      temp.append(i[1])
  return True

def grouphandsbytype(sortedinputlist):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  betterinputlist = []
  for type in types:
    typegroup = []
    for hand in sortedinputlist:
      if (hand[1] == type):
        typegroup.append(hand)
    if (typegroup != []):
      betterinputlist.append(typegroup)
  handsonly = []
  for type in betterinputlist:
    typegroup = []
    for hand in type:
      typegroup.append(hand[0])
    handsonly.append(typegroup)
  return betterinputlist, handsonly

def formatbetterinputlist(betterinputlist):
  orderedinput = []
  groupedhands = []
  for type in range(len(betterinputlist)):
    group = betterinputlist[type]
    typeorder = []
    typegroup = []
    for i in range(len(group)):
      typeorder.append([i, sorthand(group[i][0])])
    typeorder.sort(key=sortsecondindex)
    for i in typeorder:
      typegroup.append(group[i[0]])
    for i in range(len(typeorder) - 1):
      cur = typeorder[i][1]
      next = typeorder[i + 1][1]
      if isinstance(cur, list):
        cur = cur[0]
      if isinstance(next, list):
        next = next[0]
      if (cur == next):
        if not isinstance(typeorder[i][1], list):
          typeorder[i][1] = [cur]
        if not isinstance(typeorder[i + 1][1], list):
          typeorder[i + 1][1] = [next]
    orderedinput.append(typeorder)
    groupedhands.append(typegroup)
  return orderedinput, groupedhands

def gethandsneedingranking(type, typeorder, compare):
  newtypeorder = []
  editedindexes = []
  compgroups = {}
  for i in range(len(typeorder) - 1):
    cur = typeorder[i][1]
    next = typeorder[i + 1][1]
    if ((isinstance(cur, list) and isinstance(next, list)) and ((len(cur) > compare) and (len(next) > compare)) and (cur[compare] == next[compare])):
      k = str(cur[compare])
      if k in compgroups:
        compgroups[k] += 1
        newtypeorder.append([typeorder[i + 1][0], sorthand(type[typeorder[i + 1][0]][compare + 1]), i + 1])
        editedindexes.append(i + 1)
      else:
        compgroups[k] = 2
        newtypeorder.append([typeorder[i][0], sorthand(type[typeorder[i][0]][compare + 1]), i])
        newtypeorder.append([typeorder[i + 1][0], sorthand(type[typeorder[i + 1][0]][compare + 1]), i + 1])
        editedindexes.append(i)
        editedindexes.append(i + 1)
  if (compgroups == {}):
    print (repeatscheck(typeorder, True))
    print ("type:", type)
    print ("typeorder:", typeorder)
    print ("Compare:", compare)
    print ("Somethings's gone wrong here.")
  sortednewtypeorder = []
  ind = 0
  for v in compgroups.values():
    ordergroup = []
    for i in range(v):
      ordergroup.append(newtypeorder[ind + i])
    ind += v
    sortednewtypeorder.append(ordergroup)
  return sortednewtypeorder, editedindexes

def getnewindex(sharednum, temp):
  for i in range(len(sharednum)):
    if (sharednum[i][0] == temp[0]):
      return i

def sorthands(betterinputlist):
  orderedinput, groupedhands = formatbetterinputlist(betterinputlist)
  for type in range(len(groupedhands)):
    group = groupedhands[type]
    nums = orderedinput[type]
    compare = 0
    while not repeatscheck(orderedinput[type]):
      newtypeorder, editedindexes = gethandsneedingranking(group, orderedinput[type], compare)
      ind = 0
      for sharednum in newtypeorder:
        sharednum.sort(key=sortsecondindex)
        for i in range(len(sharednum)):
          oind = editedindexes[ind + i]
          if (nums[oind][0] == sharednum[i][0]):
            nums[oind][1].append(sharednum[i][1])
          else:
            temp = nums[oind]
            newindex = getnewindex(sharednum, temp)
            sharednum[newindex][2] = sharednum[i][2]
            nums[oind] = [sharednum[i][0], nums[sharednum[i][2]][1]]
            nums[sharednum[i][2]] = temp
            sharednum[i][2] = oind
            nums[oind][1].append(sharednum[i][1])
        ind += len(sharednum)
      orderedinput[type] = nums
      compare += 1
      if (compare >= 6):
        break
  return orderedinput

def rankhands(sortedhands, betterinputlist, rank):
  for type in range(len(sortedhands)):
    for hand in sortedhands[type]:
      betterinputlist[type][hand[0]][2] = rank
      rank -= 1
  return betterinputlist

def getwinnings(betterinputlist):
  winnings = []
  for type in betterinputlist:
    for hand in type:
      eq = f"{hand[2]} * {hand[3]}"
      winnings.append(eval(eq))
  return winnings

def main():
  rawinputlist = getinput()
  sortedinputlist = sortcardinfo(rawinputlist)
  betterinputlist, handsonly = grouphandsbytype(sortedinputlist)
  sortedhands = sorthands(handsonly)
  rankedhands = rankhands(sortedhands, betterinputlist, len(sortedinputlist))
  winnings = getwinnings(betterinputlist)
  print (sum(winnings))

main()
