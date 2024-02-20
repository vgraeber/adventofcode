from pathlib import Path
import copy

def getinput():
  path = path = Path(__file__).parent / "sample.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n\n")
  workflows = rawinputlist[0].split("\n")
  return workflows

def formatinput(rawworkflows):
  opppairs = {'<': ">=", '>': "<=", "==": "!=", "<=": '>', ">=": '<', "!=": "=="}
  wkflows = {}
  for workflow in rawworkflows:
    workflow = workflow.split('{')
    wkflows[workflow[0]] = {}
    rules = workflow[1].split(',')
    wkflows[workflow[0]]["rules"] = []
    for rule in rules:
      conds = rule.split(':')
      if (len(conds) == 1):
        req = []
        for otherconds in wkflows[workflow[0]]["rules"]:
          req.append([otherconds[0][0][0], opppairs[otherconds[0][0][1]], otherconds[0][0][2]])
        res = conds[0][:-1]
      else:
        req = [[conds[0][0], conds[0][1], int(conds[0][2:-1])]]
        res = conds[1]
      wkflows[workflow[0]]["rules"].append([req, res])
  return wkflows

def clean(wkflows, oneres):
  for k in wkflows.keys():
    for rule in wkflows[k]["rules"]:
      if (rule[1] in oneres):
        return False
  return True

def rem(remdict, remkey):
  try:
    remdict.pop(remkey)
  except KeyError:
    pass

def conddicts(wkflows):
  oneres = []
  first = True
  while ((not clean(wkflows, oneres)) or (first)):
    convs = 0
    for k in wkflows.keys():
      kres = []
      for rule in wkflows[k]["rules"]:
        res = rule[1]
        if res in oneres:
          rule[1] = wkflows[res]["rules"][0][1]
        elif res not in kres:
          kres.append(res)
      if (len(kres) == 1):
        oneres.append(k)
        wkflows[k]["rules"] = [[[['', "==", '']], kres[0]]]
    first = False
  for k in oneres:
    rem(wkflows, k)

def getcombos(workflows):
  endres = ['R', 'A']
  combos = []
  flowqueue = [{'x': [], 'm': [], 'a': [], 's': [], "goto": "in"}]
  while (flowqueue != []):
    reqs = flowqueue[0]
    for rule in workflows[reqs["goto"]]["rules"]:
      res = rule[1]
      newreqs = copy.deepcopy(reqs)
      for cond in rule[0]:
        newreqs[cond[0]].append([cond[1], cond[2]])
      if res not in endres:
        newreqs["goto"] = res
        flowqueue.append(newreqs)
      else:
        rem(newreqs, "goto")
        if (res == 'A'):
          combos.append(newreqs)
    flowqueue.pop(0)
  return combos

def sortfunc(cond):
  return cond[1]

def sortcombos(combos):
  for combo in combos:
    combo['x'].sort(key=sortfunc)
    combo['m'].sort(key=sortfunc)
    combo['a'].sort(key=sortfunc)
    combo['s'].sort(key=sortfunc)

def calccombos(combos, rvbounds):
  opp = {'<': ["dec", "excl"], '>': ["inc", "excl"], "<=": ["dec", "incl"], ">=": ["inc", "incl"]}
  letters = ['x', 'm', 'a', 's']
  totcombos = 0
  for combo in combos:
    for letter in letters:
      prevdir = ''
      letterbounds = [rvbounds.copy()]
      rstrcs = combo[letter]
      for rstrc in rstrcs:
        info = opp[rstrc[0]]
        dir = info[0]
        type = info[1]
        if ((dir == prevdir) or (prevdir == '')):
          if (dir == "dec"):
            if (type == "excl"):
              rstrc[1] -= 1
            letterbounds[-1][1] = rstrc[1]
          else:
            if (type == "excl"):
              rstrc[1] += 1
            letterbounds[-1][0] = rstrc[1]
        else:
          if (dir == "dec"):
            if (type == "excl"):
              rstrc[1] -= 1
            letterbounds[-1][1] = rstrc[1]
          else:
            if (type == "excl"):
              rstrc[1] += 1
            letterbounds.append([rstrc[1], rvbounds[1]])
      combo[letter] = letterbounds
    lettersums = []
    for letter in letters:
      lettersum = 0
      for inclrange in combo[letter]:
        lettersum += inclrange[1] - inclrange[0] + 1
      lettersums.append(lettersum)
    combosum = 1
    for sum in lettersums:
      combosum *= sum
    combo["combos"] = combosum
    totcombos += combosum
  print (totcombos)


def main():
  rawworkflows = getinput()
  workflows = formatinput(rawworkflows)
  conddicts(workflows)
  combos = getcombos(workflows)
  sortcombos(combos)
  rvbounds = [1, 4000]
  calccombos(combos, rvbounds)

main()
