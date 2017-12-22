import sys
import asyncio
import discord

from auth import *



client = discord.Client(max_messages=128)

print('dicebag ii connected')

@client.event
async def on_message(msg):
  print msg


