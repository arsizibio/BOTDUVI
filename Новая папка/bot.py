import discord 
from discord.ext import commands
import asyncio
import random

client = commands.Bot(command_prefix = '!' )



token = open('token.txt', 'r').readline()
client.run(token)