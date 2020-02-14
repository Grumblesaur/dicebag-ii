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

invite_url = '''https://discordapp.com/oauth2/authorize?&client_id=674076495425044511&scope=bot&permissions=0'''

source_url = '''https://github.com/Grumblesaur/atropos'''

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
  
  if rolls or orders or helptext:
    reply = 'Dicebag has been deprecated. Please use Atropos instead.'
    reply += '\n  Invite link: {}'.format(invite_url)
    reply += '\n  Source code: {}'.format(source_url)
    await msg.channel.send(reply)

if __name__ == '__main__':
  global_vars.load_state()
  private_vars.load_state()
  print('dicebag initialized')
  client.run(bot_token)
  

