import sys
import asyncio
import discord
import time

import dice
import info
import turns
import global_vars

from auth import *

client = discord.Client(max_messages=128)
current_time = 0
last_time    = 0

@client.event
async def on_message(msg):
  global current_time
  global last_time
  current_time = time.time()
  try:
    name = msg.author.nick
  except AttributeError:
    name = msg.author.name
  rolls = dice.scan(msg.content, name)
  orders = turns.scan(msg.content)
  helptext = info.scan(msg.content)
  
  if rolls:
    await client.send_message(msg.channel, dice.notify(rolls, msg))

  if orders:
    await client.send_message(msg.channel, turns.notify(rolls))
  
  if helptext:
    await client.send_message(msg.channel, helptext)
  
  # save state every 5 minutes
  if current_time - last_time > 300:
    global_vars.save_state()
    last_time = time.time()

global_vars.load_state()
client.run(bot_token)
  

