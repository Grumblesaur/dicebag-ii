import global_vars

class TurnError(Exception):
  pass

class TurnOrder(object):
  def __repr__(self):
    return '"%s"' % '::::'.join(map(repr, [
      self.order,
      self.new_waiting,
      self.dead_waiting,
      self.turns,
      self.rounds,
      self.active,
      self.new,
      self.dead
    ]))
  
  def __init__(self, serialized=None):
    if not serialized:
      self.order        = []
      self.new_waiting  = []
      self.dead_waiting = []
      self.turns        = 0
      self.rounds       = 1
      self.active       = False
      self.new          = False
      self.dead         = False
    else:
      initialized = serialized.split('::::')
      self.order = eval(initialized[0])
      self.new_waiting = eval(initialized[1])
      self.dead_waiting = eval(initialized[2])
      self.turns = int(eval(initialized[3]))
      self.rounds = int(eval(initialized[4]))
      self.active = bool(eval(initialized[5]))
      self.new = bool(eval(initialized[6]))
      self.dead = bool(eval(initialized[7]))
  
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
    return [("active turn order global_vars.turn_tracker:", "no argument")] + (
      list(
        zip(
          list(global_vars.turn_tracker.keys()), [
            len(
              global_vars.turn_tracker[l]
            ) for l in global_vars.turn_tracker.keys()
          ]
        )
      )
    )
  
  if tokens[0] == "create":
    global_vars.turn_tracker[tokens[1]] = TurnOrder()
    print('create')
    return[("Created new turn order with name '%s'." % tokens[1], "create")]
  if tokens[0] == "add":
    global_vars.turn_tracker[tokens[1]].add(tokens[2], int(tokens[3]))
    return [("Added '%s' to the turn order '%s'." % tuple(
      tokens[2:0:-1]
    ), "add")]
  if tokens[0] == "remove":
    global_vars.turn_tracker[tokens[1]].remove(tokens[2])
    return [
      ("Removed '%s' from the turn order '%s'." % tokens[2:0:-1], "remove")
    ]
  if tokens[0] == "start":
    global_vars.turn_tracker[tokens[1]].start()
    return [("Started turn order '%s'." % tokens[1], "start")]
  if tokens[0] == "next":
    if not global_vars.turn_tracker[tokens[1]].active:
      raise TurnOrderError("Start the turn order to advance it.")
    actor = global_vars.turn_tracker[tokens[1]].rotate()
    genitive = '' if actor.endswith('s') else 's'
    return [("It's %s'%s turn." % (actor, genitive), "next")]
  if tokens[0] == "check":
    if not global_vars.turn_tracker[tokens[1]].active:
      raise TurnOrderError("Start the turn order to check the next player.")
    actor = global_vars.turn_tracker[tokens[1]].check()
    return [("%s is on deck." % actor, "check")]
  if tokens[0] == "view":
    current_round, actors = global_vars.turn_tracker[tokens[1]].view()
    return [
      ("It's round %s in turn order '%s'."%(current_round,tokens[1]),"view")
    ] + actors
  if tokens[0] == "stop":
    global_vars.turn_tracker[tokens[1]].stop()
    return [("Stopped and reset turn order '%s'." % tokens[1], "stop")]
  if tokens[0] == "clear":
    try:
      e = None
      global_vars.turn_tracker[tokens[1]].clear()
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




