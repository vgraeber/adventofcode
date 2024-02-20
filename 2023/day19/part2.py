from pathlib import Path
import operator

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

def sortcombos(workflows, ratingvalbounds):
  endres = ['R', 'A']
  currwkflow = "in"
  totnumcombos = pow(ratingvalbounds[1], 4)
  combos = []
  flowqueue = []
  for rule in workflows[currwkflow]["rules"]:
    res = rule[1]
    if res not in endres:
      continue
    else:
      currwkflow = res
"""
def managebeam(origarr, beamarr, dir, pos):
  dirqueue = []
  while dir is not None:
    dir = getnewbeamdir(origarr, beamarr, dir, pos)
    if isinstance(dir, list):
      dirqueue.append([dir[1], pos.copy()])
      dir = dir[0]
    elif dir is None:
      if (len(dirqueue) > 0):
        dir = dirqueue[0][0]
        pos = dirqueue[0][1]
        dirqueue.pop(0)
      else:
        return
    pos = movebeam(dir, pos)
    while not inbounds(origarr, pos):
      if (len(dirqueue) > 0):
        dir = dirqueue[0][0]
        pos = dirqueue[0][1]
        dirqueue.pop(0)
        pos = movebeam(dir, pos)
      else:
        return
"""
opp = {'<': operator.lt, '>': operator.gt, "==": operator.eq, "<=": operator.le, ">=": operator.ge, "!=": operator.ne}

def main():
  rawworkflows = getinput()
  ratingvalbounds = [1, 4000]
  workflows = formatinput(rawworkflows)
  conddicts(workflows)
  #combos = sortcombos(workflows, ratingvalbounds)
  for flowname, flow in workflows.items():
    print (flowname, flow)

main()
