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
  ranks = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
  return ranks.index(card)

def gethandtype(hdict):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  type = 6
  hvals = list(hdict.values())
  hvals.sort(reverse=True)
  if 'J' in hdict:
    if (max(hdict, key=hdict.get) != 'J'):
      hvals[0] += hdict['J']
    else:
      if (len(hvals) > 1):
        hvals[1] += hdict['J']
        hvals.pop(0)
  if (hvals[0] == 5):
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

def sortbytype(somedict):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  return types.index(somedict["type"])

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
    type = gethandtype(hdict)
    bid = int(lessrawinfo[1])
    sortedinputlist.append({"hand": lessrawinfo[0], "type": type, "bid": bid})
  sortedinputlist.sort(key=sortbytype)
  return sortedinputlist

def grouphandsbytype(sortedinputlist):
  types = ["five", "four", "full", "three", "two", "one", "high"]
  betterinputlist = []
  handsonly = []
  for type in types:
    typegroup = []
    handgroup = []
    for hand in sortedinputlist:
      if (hand["type"] == type):
        typegroup.append(hand)
        handgroup.append(list(hand["hand"]))
    betterinputlist.append(typegroup)
    handsonly.append(handgroup)
  return betterinputlist, handsonly

def sortsecondindex(somelist):
  return somelist[1][0]

def getnumvalsofhands(handsonly):
  handnuminput = []
  ind = 0
  for type in handsonly:
    typeorder = []
    for i in range(len(type)):
      handnumvals = []
      for j in type[i]:
        handnumvals.append(sorthand(j))
      typeorder.append([[ind, i], handnumvals])
    typeorder.sort(key=sortsecondindex)
    handnuminput.append(typeorder)
    ind += 1
  return handnuminput

def orderhands(handnuminput):
  orderedinput = []
  for type in handnuminput:
    for i in range(len(type)):
      for j in range(1, len(type) - i):
        current = type[i]
        next = type[i + j]
        for ind in range(5):
          if (current[1][ind] < next[1][ind]):
            break
          elif (current[1][ind] > next[1][ind]):
            type[i] = next
            type[i + j] = current
            break
    orderedinput.append(type)
  return orderedinput

def sorthands(handsonly):
  handnuminput = getnumvalsofhands(handsonly)
  orderedinput = orderhands(handnuminput)
  return orderedinput

def rankhands(sortedhands, betterinputlist, rank):
  for type in sortedhands:
    for hand in type:
      betterinputlist[hand[0][0]][hand[0][1]]["rank"] = rank
      rank -= 1
  return betterinputlist

def getwinnings(sortedhands, betterinputlist):
  winnings = 0
  for type in sortedhands:
    for hand in type:
      eq = f"{betterinputlist[hand[0][0]][hand[0][1]]['rank']} * {betterinputlist[hand[0][0]][hand[0][1]]['bid']}"
      betterinputlist[hand[0][0]][hand[0][1]]["winnings"] = eval(eq)
      winnings += eval(eq)
  return betterinputlist, winnings

def sortbyrank(somedict):
  return somedict["rank"]

def printinfo(betterinputlist):
  for type in betterinputlist:
    type.sort(key=sortbyrank, reverse=True)
    for hand in type:
      print (hand)

def main():
  rawinputlist = getinput()
  sortedinputlist = sortcardinfo(rawinputlist)
  betterinputlist, handsonly = grouphandsbytype(sortedinputlist)
  sortedhands = sorthands(handsonly)
  rankedhands = rankhands(sortedhands, betterinputlist, len(sortedinputlist))
  completeinputlist, winnings = getwinnings(sortedhands, rankedhands)
  #printinfo(completeinputlist)
  print (winnings)

main()
