from pathlib import Path

def getinput():
  path = Path(__file__).parent / "input.txt"
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

def sortbytype(l):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  return types.index(l[1])

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
  sortedinputlist.sort(key=sortbytype)
  return sortedinputlist

def sortsecondindex(l):
  return l[1]

def repeatscheck(inputlist):
  temp = []
  for i in inputlist:
    if i[1] in temp:
      return False
    else:
      temp.append(i[1])
  return True

def grouphandsbytype(sortedinputlist):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  betterinputlist = []
  handsonly = []
  for type in types:
    typegroup = []
    handgroup = []
    for hand in sortedinputlist:
      if (hand[1] == type):
        typegroup.append(hand)
        handgroup.append(hand[0])
    betterinputlist.append(typegroup)
    handsonly.append(handgroup)
  return betterinputlist, handsonly

def getnumvalsofhands(handsonly):
  orderedinput = []
  for type in handsonly:
    typeorder = []
    for i in range(len(type)):
      typeorder.append([i, [sorthand(type[i][0])]])
    typeorder.sort(key=sortsecondindex)
    orderedinput.append(typeorder)
  return orderedinput

def gethandsneedingranking(group, nums, compare):
  newtypeorder = []
  editedindexes = []
  compgroups = {}
  for i in range(len(nums) - 1):
    cur = nums[i][1]
    sharedcards = []
    if (len(cur) > compare):
      for j in range(1, len(nums) - i):
        next = nums[i + j][1]
        if ((len(next) > compare) and (cur == next)):
          k = str(cur[compare])
          if ((k in compgroups) and ((i + j) not in editedindexes)):
            compgroups[k] += 1
            sharedcards.append([nums[i + j][0], sorthand(group[nums[i + j][0]][compare + 1]), i + j])
            editedindexes.append(i + j)
          elif k not in compgroups:
            compgroups[k] = 2
            sharedcards.append([nums[i][0], sorthand(group[nums[i][0]][compare + 1]), i])
            sharedcards.append([nums[i + j][0], sorthand(group[nums[i + j][0]][compare + 1]), i + j])
            editedindexes.append(i)
            editedindexes.append(i + 1)
    if (sharedcards != []):
      newtypeorder.append(sharedcards)
  if (compgroups == {}):
    print ("Somethings's gone wrong here.")
  return newtypeorder, editedindexes

def getnewindex(sharednum, temp):
  for i in range(len(sharednum)):
    if (sharednum[i][0] == temp[0]):
      return i

def sorthands(handsonly):
  orderedinput = getnumvalsofhands(handsonly)
  for type in range(len(handsonly)):
    group = handsonly[type]
    nums = orderedinput[type]
    compare = 0
    while not repeatscheck(nums):
      newtypeorder, editedindexes = gethandsneedingranking(group, nums, compare)
      ind = 0
      for sharednum in newtypeorder:
        sharednum.sort(key=sortsecondindex)
        for i in range(len(sharednum)):
          oind = editedindexes[ind + i]
          if (nums[oind][0] == sharednum[i][0]):
            nums[oind][1].append(sharednum[i][1])
          else:
            oldinfo = nums[oind]
            oldindex = getnewindex(sharednum, oldinfo)
            newindex = sharednum[i][2]
            nums[oind] = nums[sharednum[i][2]]
            nums[newindex] = oldinfo
            sharednum[i][2] = sharednum[oldindex][2]
            sharednum[oldindex][2] = newindex
            nums[oind][1].append(sharednum[i][1])
        ind += len(sharednum)
      orderedinput[type] = nums
      compare += 1
      if (compare >= 6):
        print ("exceeding length of poker hand")
        break
  return orderedinput

def sortbyrank(l):
  return l[2]

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
