from global_vars import turn_tracker as tracker

class TurnError(Exception):
  pass

class TurnOrder(object):
  def __init__(self):
    self.order        = []
    self.new_waiting  = []
    self.dead_waiting = []

    self.turns        = 0
    self.rounds       = 1
    
    self.active       = False
    self.new          = False
    self.dead         = False

  def __len__(self):
    return len(self.order)

  def __getitem__(self, index):
    return self.order[index]

  def add(self, name, initiative):
    if not self.active:
      self.order.append((name, initiative))
    else:
      self.new_waiting.append((name, initiative))
      self.new = True

  def remove(self, name):
    if not self.active:
      self.order.remove(name)
    else:
      self.dead_waiting += [actor for actor in self.order if name in actor]
      self.dead = True

  def rotate(self):
    out = self[self.turns % len(self)][0]
    self.turns += 1
    if self.turns % len(self) == 0:
      self.rounds += 1
      if self.dead:
        self.order = list(set(self.order) - set(self.dead_waiting))
        self.dead_waiting = []
        self.dead = False
      if self.new:
        self.order += self.new_waiting
        self.new_waiting = []
        self.new = False
      self.turns = 0
      self.order = sorted(self.order, key=lambda x: x[1], reverse=True)
    return out

  def check(self):
    return self[self.turns % len(self)][0]

  def view(self):
    return (self.rounds, self.order)

  def start(self):
    self.order = sorted(self.order, key=lambda x: x[1], reverse=True)
    self.active = True

  def stop(self):
    self.active = self.dead = self.new = False
    self.turns = 0
    self.rounds = 1
    self.order += self.new_waiting
    self.order = list(set(self.order) - set(self.dead_waiting))
    self.new_waiting = self.dead_waiting = []

  def clear(self):
    if self.active:
      raise TurnOrderError("Stop the turn order to clear it.")
    self.order = []

def scan(msg):
  if "!initiative" not in msg:
    return []
  try:
    tokens = msg.split("!initiative")[1].split()
    tokens[1] = tokens[1].lower()
  except IndexError as e:
    return [("active turn order trackers:", "no argument")] + list(
      zip(list(tracker.keys()), [len(tracker[l] for l in tracker.keys())])
    )
  
  if tokens[0] == "create":
    tracker[tokens[1]] = TurnOrder()
    return[("Created new turn order with name '%s'." % tokens[1], "create")]
  if tokens[0] == "add":
    tracker[tokens[1]].add(tokens[2], int(tokens[3]))
    return [("Added '%s' to the turn order '%s'." % tuple(
      tokens[2:0:-1]
    ), "add")]
  if tokens[0] == "remove":
    tracker[tokens[1]].remove(tokens[2])
    return [
      ("Removed '%s' from the turn order '%s'." % tokens[2:1:-1], "remove")
    ]
  if tokens[0] == "start":
    tracker[tokens[1]].start()
    return [("Started turn order '%s'." % tokens[1], "start")]
  if tokens[0] == "next":
    if not tracker[tokens[1]].active:
      raise TurnOrderError("Start the turn order to advance it.")
    actor = tracker[tokens[1]].rotate()
    genitive = '' if actor.endswith('s') else 's'
    return [("It's %s'%s turn." % (actor, genitive), "next")]
  if tokens[0] == "check":
    if not tracker[tokens[1]].active:
      raise TurnOrderError("Start the turn order to check the next player.")
    actor = tracker[tokens[1]].check()
    return [("%s is on deck." % actor, "check")]
  if tokens[0] == "view":
    current_round, actors = tracker[tokens[1]].view()
    return [
      ("It's round %s in turn order '%s'."%(current_round,tokens[1]),"view")
    ] + actors
  if tokens[0] == "stop":
    tracker[tokens[1]].stop()
    return [("Stopped and reset turn order '%s'." % tokens[1], "stop")]
  if tokens[0] == "clear":
    try:
      e = None
      tracker[tokens[1]].clear()
    except TurnOrderError as e:
      pass
    finally:
      return [("%s." % e or ("Turn order '%s' cleared."%token[1]),"clear")]
  return []

def notify(pairs):
  print('\t', pairs)
  out = "%s (%s)" % pairs[0]
  out = out + '\n' + '\n'.join(
      ["\t%s (%s)" % p for p in pairs[1:]]) if len(pairs) > 1 else out
  return out




