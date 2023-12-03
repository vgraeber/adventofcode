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
        yourcardwinningnums.append(num)
    yourwinningnums.append(yourcardwinningnums)
  return yourwinningnums

def getnumcards(yourwinningnums):
  numcards = [1]  * len(yourwinningnums)
  for card in range(len(yourwinningnums)):
    for i in range(numcards[card]):
      for j in range(len(yourwinningnums[card])):
        numcards[card + (j + 1)] += 1
  return numcards

def main():
  rawinputlist = getinput()
  sortedinputlist = sortcardinfo(rawinputlist)
  yourwinningnums = getyourwinningnums(sortedinputlist)
  numcards = getnumcards(yourwinningnums)
  print(sum(numcards))

main()
