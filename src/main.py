import sys
import asyncio
import discord
import time

import dice
import info
import turns
import global_vars
import private_vars

from auth import *

client = discord.Client(max_messages=128)
current_time = 0
last_save    = 0
last_backup  = 0

@client.event
async def on_message(msg):
  global current_time
  global last_save
  global last_backup
  current_time = time.time()
  name = msg.author.name
  try:
    nick = msg.author.nick
  except AttributeError:
    nick = msg.author.name
  rolls = dice.scan(msg.content, nick, name)
  orders = turns.scan(msg.content)
  helptext = info.scan(msg.content)
  
  if rolls:
    await client.send_message(msg.channel, dice.notify(rolls, msg))

  if orders:
    await client.send_message(msg.channel, turns.notify(orders))
  
  if helptext:
    await client.send_message(msg.channel, helptext)
  
  if msg.content.startswith('!save'):
    global_vars.save_state()
    global_vars.backup_state()
  
  # save state every 5 minutes
  if current_time - last_save > 300:
    global_vars.save_state()
    private_vars.save_state()
    last_save = time.time()
    print('globals saved')
  if current_time - last_backup > 1800:
    global_vars.backup_state()
    private_vars.backup_state()
    last_backup = current_time
    print('globals backed up')
  
if __name__ == '__main__':
  global_vars.load_state()
  private_vars.load_state()
  client.run(bot_token)
  

