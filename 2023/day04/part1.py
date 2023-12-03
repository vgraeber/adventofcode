from pathlib import Path

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  return rawinputlist

def sortcardinfo(rawinputlist):
  sortedinputlist = []
  for line in rawinputlist:
    rawnuminfo = line.split(": ")[1]
    sortednuminfo = rawnuminfo.split(' | ')
    sortedinputlist.append([sortednuminfo[0].split(), sortednuminfo[1].split()])
  return sortedinputlist

def getyourwinningnums(sortedinputlist):
  yourwinningnums = []
  for card in sortedinputlist:
    yourcardwinningnums = []
    for num in card[1]:
      if num in card[0]:
        yourcardwinningnums.append(int(num))
    yourwinningnums.append(yourcardwinningnums)
  return yourwinningnums

def getcardpointvalues(yourwinningnums):
  cardpointvals = []
  for card in yourwinningnums:
    val = 2 ** (len(card) - 1)
    if (len(card) == 0):
      val = 0
    cardpointvals.append(val)
  return cardpointvals

def main():
  rawinputlist = getinput()
  sortedinputlist = sortcardinfo(rawinputlist)
  yourwinningnums = getyourwinningnums(sortedinputlist)
  cardpointvals = getcardpointvalues(yourwinningnums)
  print(sum(cardpointvals))

main()
