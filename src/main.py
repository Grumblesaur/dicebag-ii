import sys
import asyncio
import discord
import time

import dice
import turns
import global_vars

from auth import *

current_time = 0
last_time    = 0

@client.event
async def on_message(msg):
  last_time = current_time
  current_time = time.localtime()
  rolls = dice.scan(msg.content)
  turns = turns.scan(msg.content)

  if rolls:
    await client.send_message(msg.channel, dice.message(rolls, msg))

  if turns:
    await client.send_message(msg.channel, turns.message(rolls, msg))
  
  
  # save state every 5 minutes
  if current_time - last_time > 300:
    global_vars.save_state()

if __name__ == '__main__':
  global_vars.load_state()
  client = discord.Client(max_messages=128)
  client.run(bot_token)
  

