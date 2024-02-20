from pathlib import Path
import operator

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n\n")
  workflows = rawinputlist[0].split("\n")
  parts = rawinputlist[1].split("\n")
  parts.pop()
  return workflows, parts

def formatinput(rawworkflows, rawparts):
  wkflows = {}
  parts = []
  for workflow in rawworkflows:
    workflow = workflow.split('{')
    wkflows[workflow[0]] = {}
    rules = workflow[1].split(',')
    wkflows[workflow[0]]["rules"] = []
    for rule in rules:
      conds = rule.split(':')
      if (len(conds) == 1):
        req = ["res", "==", '']
        res = conds[0][:-1]
      else:
        req = [conds[0][0], conds[0][1], int(conds[0][2:])]
        res = conds[1]
      wkflows[workflow[0]]["rules"].append([req, res])
  for part in rawparts:
    part = part[1:-1]
    categories = part.split(',')
    currpartdict = {"res": ''}
    for category in categories:
      vals = category.split('=')
      currpartdict[vals[0]] = int(vals[1])
    parts.append(currpartdict)
  return wkflows, parts

def runthroughrules(rules, part):
  ops = {'<': operator.lt, '>': operator.gt, "==": operator.eq}
  for rule in rules:
    if (ops[rule[0][1]](part[rule[0][0]], rule[0][2])):
      return rule[1]

def sortparts(workflows, parts):
  partres = ['R', 'A']
  for part in parts:
    currwkflow = "in"
    while (currwkflow != "next part"):
      res = runthroughrules(workflows[currwkflow]["rules"], part)
      if res in partres:
        part["res"] = res
        currwkflow = "next part"
      else:
        currwkflow = res

def sumaccptd(parts):
  sum = 0
  for part in parts:
    if (part["res"] == 'A'):
      sum += part['x'] + part['m'] + part['a'] + part['s']
  return sum

def main():
  rawworkflows, rawparts = getinput()
  workflows, parts = formatinput(rawworkflows, rawparts)
  sortparts(workflows, parts)
  sum = sumaccptd(parts)
  print (sum)

main()
