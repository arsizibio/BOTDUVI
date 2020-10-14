import discord, os, asyncio, requests, time, random
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
from io import BytesIO
import lib.errors as silentic_errors
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

class Economy(commands.Cog):
    '''cogs.economy.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.economy.desc'
        self.thumbnail = 'economy'

    def credit_time_passed(self, timestamp: float):
        return (datetime.now() - datetime.utcfromtimestamp(timestamp)).total_seconds() / 60 
    def get_credit_amount(self, user):
        credit = self.bot.load_json('data/credit_claimed.json')
        if str(user.guild.id) not in credit: return 0
        if str(user.id) not in credit[str(user.guild.id)]: return 0
        return self.get_bank(user) + round(self.credit_time_passed(credit[str(user.guild.id)][str(user.id)]))
    def get_reputation(self, user):
        reputation = self.bot.load_json('data/reputation.json')
        if str(user.guild.id) not in reputation: return 0.0
        if str(user.id) not in reputation[str(user.guild.id)]: return 0.0
        return reputation[str(user.guild.id)][str(user.id)]
    def set_reputation(self, user, amount: float):
        reputation = self.bot.load_json('data/reputation.json')
        if str(user.guild.id) not in reputation: reputation[str(user.guild.id)] = {}
        reputation[str(user.guild.id)][str(user.id)] = abs(amount)
        self.bot.write_json('data/reputation.json', reputation)
    def get_coins(self, user):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['coins']: return 0
        if str(user.id) not in coins['coins'][str(user.guild.id)]: return 0
        return coins['coins'][str(user.guild.id)][str(user.id)]
    def get_boost(self, user):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['boost']: return 0
        if str(user.id) not in coins['boost'][str(user.guild.id)]: return 0
        return coins['boost'][str(user.guild.id)][str(user.id)]
    def set_coins(self, user, amount: int):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['coins']: coins['coins'][str(user.guild.id)] = {}
        coins['coins'][str(user.guild.id)][str(user.id)] = abs(amount)
        self.bot.write_json('data/coins.json', coins)
    def get_bank(self, user):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['bank']: return 0
        if str(user.id) not in coins['bank'][str(user.guild.id)]: return 0
        return coins['bank'][str(user.guild.id)][str(user.id)]
    def set_boost(self, user, amount: int):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['boost']: coins['boost'][str(user.guild.id)] = {}
        coins['boost'][str(user.guild.id)][str(user.id)] = abs(amount)
        self.bot.write_json('data/coins.json', coins)
    def set_bank(self, user, amount: int):
        coins = self.bot.load_json('data/coins.json')
        if str(user.guild.id) not in coins['bank']: coins['bank'][str(user.guild.id)] = {}
        coins['bank'][str(user.guild.id)][str(user.id)] = abs(amount)
        self.bot.write_json('data/coins.json', coins)

    async def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Guild only')
        if ctx.author.guild_permissions.administrator == False:
            raise commands.MissingPermissions(['administrator'])
        return ctx.author.guild_permissions.administrator
    
    @commands.command(name='set-balance', aliases=['setbal'])
    async def setbalance(self, ctx, user: discord.Member, new_balance: int):
        '''eco.setbal.desc'''
        self.set_coins(user, new_balance)
        await ctx.message.add_reaction('✅')
    
    @commands.command(name='give-money', aliases=['give-coins'])
    async def addbalance(self, ctx, user: discord.Member, amount: int):
        '''eco.givebal.desc'''
        self.set_coins(user, self.get_coins(user)+amount)
        await ctx.message.add_reaction('✅')
    
    @commands.command(name='remove-money', aliases=['remove-coins'])
    async def removebal(self, ctx, user: discord.Member, amount: int):
        '''eco.removebal.desc'''
        if self.get_coins(user)-amount < 0:
            self.set_coins(user, 0)
        else:
            self.set_coins(user, self.get_coins(user)-amount)
        await ctx.message.add_reaction('✅')
    
    @commands.command(name='set-reputation', aliases=['setrep'])
    async def setreputation(self, ctx, user: discord.Member, new_reputation: float):
        '''eco.setrep.desc'''
        if new_reputation > 999: new_reputation = 999
        self.set_reputation(user, new_reputation)
        await ctx.message.add_reaction('✅')

    @commands.command(name='set-boost', aliases=['setboost'])
    async def setboost(self, ctx, user: discord.Member, boost: int):
        '''eco.setboost.desc'''
        if boost > 999: boost = 999
        self.set_boost(user, boost)
        await ctx.message.add_reaction('✅')
    
    @commands.command(name='reset-cooldown', aliases=['resetcooldown'])
    async def resetcooldown(self, ctx):
        '''eco.resetcd.desc'''
        confirm = await ctx.confirm(discord.Embed(title=ctx.l10n('eco.resetcd.confirm')))
        if not confirm: return
        cooldown = self.bot.load_json('data/cooldown.json')
        if str(ctx.guild.id) in cooldown: del cooldown[str(ctx.guild.id)]
        self.bot.write_json('data/cooldown.json', cooldown)
        await ctx.message.add_reaction('✅')
        

def setup(bot: Bot):
    bot.add_cog(Economy(bot))