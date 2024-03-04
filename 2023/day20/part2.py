from pathlib import Path
import copy

def getinput():
  path = path = Path(__file__).parent / "input.txt"
  inputfile = open(path, 'r')
  rawinput = inputfile.read()
  inputfile.close()
  rawinputlist = rawinput.split("\n")
  rawinputlist.pop()
  lessrawinputlist = [line.split(" -> ") for line in rawinputlist]
  filteredinputlist = [[[line[0][0], line[0][1:]], line[1].split(", ")] for line in lessrawinputlist]
  for line in range(len(filteredinputlist)):
    if (filteredinputlist[line][0] == ["b", "roadcaster"]):
      filteredinputlist[line][0] = ["broadcast", "broadcaster"]
  filteredinputlist.insert(0, [["button", "button"], ["broadcaster"]])
  return filteredinputlist

def findconnections(inputlist, lookfor):
  connections = []
  for line in inputlist:
    dests = line[1]
    if lookfor in dests:
      connections.append(line[0][1])
  return connections

def formatinput(inputlist):
  newinputlist = []
  for line in inputlist:
    module = {"type": line[0][0], "name": line[0][1], "destinations": line[1]}
    if (module["type"] == '%'):
      module["state"] = "off"
    elif (module["type"] == '&'):
      memory = {}
      connections = findconnections(inputlist, module["name"])
      for connection in connections:
        memory[connection] = "low"
      module["connections"] = memory
    newinputlist.append(module)
  return newinputlist

def conjunctmodcheck(memory):
  for v in memory.values():
    if (v == "low"):
      return "high"
  return "low"

def findmodule(inputlist, name):
  for module in inputlist:
   if (module["name"] == name):
     return module

def handlepulse(module, pulse):
  newpulse = []
  if (module["type"] == '%'):
    flip = {"on": "off", "off": "on"}
    if (pulse[1] == "low"):
      module["state"] = flip[module["state"]]
      if (module["state"] == "on"):
        newpulse = [module["name"], "high"]
      else:
        newpulse = [module["name"], "low"]
  elif (module["type"] == '&'):
    module["connections"][pulse[0]] = pulse[1]
    newpulse = [module["name"], conjunctmodcheck(module["connections"])]
  elif (module["type"] == "broadcast"):
    newpulse = [module["name"], pulse[1]]
  return newpulse

def sendpulse(inputlist):
  pulsequeue = [["button", "low"]]
  totalpulses = {"low": 0, "high": 0}
  end = False
  for pulse in pulsequeue:
    module = findmodule(inputlist, pulse[0])
    for dest in module["destinations"]:
      totalpulses[pulse[1]] += 1
      newmod = findmodule(inputlist, dest)
      if ((pulse[1] == "low") and (dest == "rx")):
        end = True
      if (newmod is not None):
        newpulse = handlepulse(newmod, pulse)
        if (newpulse != []):
          pulsequeue.append(newpulse)
  return totalpulses, end

def getpulsecycle(inputlist):
  totalpulses = []
  pulsecyc, end = sendpulse(inputlist)
  totalpulses.append(pulsecyc)
  while (not end):
    pulsecyc, end = sendpulse(inputlist)
    totalpulses.append(pulsecyc)
  return totalpulses

def main():
  inputlist = getinput()
  inputlist = formatinput(inputlist)
  pulsecyc = getpulsecycle(inputlist)
  totalpulses = {"low": 0, "high": 0}
  for i in range(len(pulsecyc)):
    totalpulses["low"] += pulsecyc[i]["low"]
    totalpulses["high"] += pulsecyc[i]["high"]
  print (totalpulses["low"] * totalpulses["high"])

main()
