import discord, random
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
import lib.errors as silentic_errors

class Fun(commands.Cog):
    '''cogs.fun.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.fun.desc'
        self.thumbnail = 'fun'

    @commands.command(name='randomname')
    async def randomname(self, ctx):
        '''randomname.desc'''
def setup(bot: Bot):
    bot.add_cog(Fun(bot))