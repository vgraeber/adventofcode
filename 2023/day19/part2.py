from pathlib import Path
import copy

def getinput():
  path = path = Path(__file__).parent / "input.txt"
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
    rules = workflow[1][:-1].split(',')
    wkflows[workflow[0]]["rules"] = []
    for rule in rules:
      conds = rule.split(':')
      if (len(conds) == 1):
        req = []
        for otherconds in wkflows[workflow[0]]["rules"][-1][0]:
          req.append([otherconds[0], otherconds[1], otherconds[2]])
        req[-1][1] = opppairs[req[-1][1]]
        res = conds[0]
      else:
        req = []
        if (wkflows[workflow[0]]["rules"] != []):
          for otherconds in wkflows[workflow[0]]["rules"][-1][0]:
            req.append([otherconds[0], otherconds[1], otherconds[2]])
          req[-1][1] = opppairs[req[-1][1]]
        req.append([conds[0][0], conds[0][1], int(conds[0][2:])])
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
    for k in wkflows.keys():
      kres = []
      for rule in wkflows[k]["rules"]:
        res = rule[1]
        if res in oneres:
          rule[1] = wkflows[res]["rules"][0][1]
          kres.append(rule[1])
        elif res not in kres:
          kres.append(res)
      if (len(kres) == 1):
        oneres.append(k)
        wkflows[k]["rules"] = [[[['', "==", '']], kres[0]]]
    first = False
  for k in oneres:
    rem(wkflows, k)

def checkvalidity(newreqs, letter, sign, num):
  opp = {'<': ["dec", "excl"], '>': ["inc", "excl"], "<=": ["dec", "incl"], ">=": ["inc", "incl"]}
  dir = opp[sign][0]
  type = opp[sign][1]
  rstrc = newreqs[letter]
  if (rstrc[0] <= num <= rstrc[1]):
    if (type == "incl"):
      if (dir == "dec"):
        rstrc[1] = num
      else:
        rstrc[0] = num
      return True
    else:
      if (dir == "dec"):
        rstrc[1] = num - 1
      else:
        rstrc[0] = num + 1
      return True
  return False

def getcombos(workflows, rvs):
  endres = ['R', 'A']
  combos = []
  flowqueue = [{'x': [rvs[0], rvs[1]], 'm': [rvs[0], rvs[1]], 'a': [rvs[0], rvs[1]], 's': [rvs[0], rvs[1]], "goto": "in", "path": ["in"]}]
  while (flowqueue != []):
    reqs = flowqueue[0]
    for rule in workflows[reqs["goto"]]["rules"]:
      res = rule[1]
      newreqs = copy.deepcopy(reqs)
      isvalid = True
      for cond in rule[0]:
        if not checkvalidity(newreqs, cond[0], cond[1], cond[2]):
          isvalid = False
          break
      if isvalid:
        if res not in endres:
          newreqs["goto"] = res
          newreqs["path"].append(res)
          flowqueue.append(newreqs)
        else:
          rem(newreqs, "goto")
          newreqs["path"].append(res)
          if (res == 'A'):
            combos.append(newreqs)
    flowqueue.pop(0)
  return combos

def calccombos(combos):
  letters = ['x', 'm', 'a', 's']
  combosumsum = 0
  totalcombos = 4000 ** 4
  for combo in combos:
    combosum = 1
    for letter in letters:
      combosum *= combo[letter][1] - combo[letter][0] + 1
    combo["combos"] = combosum
    combosumsum += combosum
  print (combosumsum)

def main():
  rawworkflows = getinput()
  workflows = formatinput(rawworkflows)
  conddicts(workflows)
  rvbounds = [1, 4000]
  combos = getcombos(workflows, rvbounds)
  calccombos(combos)

main()
