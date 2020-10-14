import discord, os, asyncio, requests, time, random
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
from io import BytesIO
import lib.errors as silentic_errors
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import lib.checks as checks

class Economy(commands.Cog):
    '''cogs.economy.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.economy.desc'
        self.thumbnail = 'economy'
        self.font = ImageFont.truetype("assets/font/Comfortaa.ttf", 35)


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.guild or msg.author.bot: return
        lvl = self.bot.load_json('data/lvl_enabled.json')
        if str(msg.guild.id) not in lvl: return
        if not lvl[str(msg.guild.id)]: return
        levels = self.bot.load_json('data/levels.json')
        if str(msg.guild.id) not in levels: levels[str(msg.guild.id)] = {}
        if str(msg.author.id) not in levels[str(msg.guild.id)]: levels[str(msg.guild.id)][str(msg.author.id)] = {"xp": 0, "lvl": 1}
        levels[str(msg.guild.id)][str(msg.author.id)]["xp"] += 1
        if levels[str(msg.guild.id)][str(msg.author.id)]["xp"] >= levels[str(msg.guild.id)][str(msg.author.id)]["lvl"] * 10:
            ctx = await self.bot.get_context(msg)
            levels[str(msg.guild.id)][str(msg.author.id)]["xp"] = 0
            levels[str(msg.guild.id)][str(msg.author.id)]["lvl"] += 1
            await ctx.send(ctx.l10n('lvl.new_level', lvl=levels[str(msg.guild.id)][str(msg.author.id)]["lvl"]))
        self.bot.write_json('data/levels.json', levels)

    @commands.command(name='lvl', aliases=['level'])
    @commands.guild_only()
    async def level(self, ctx, user: discord.Member = None):
        '''lvl.lvl.desc'''
        lvl = self.bot.load_json('data/lvl_enabled.json')
        if str(ctx.guild.id) not in lvl: raise silentic_errors.LevelingIsDisabled('Leveling is disabled on this guild')
        if not lvl[str(ctx.guild.id)]: raise silentic_errors.LevelingIsDisabled('Leveling is disabled on this guild')
        if not user: user = ctx.author
        levels = self.bot.load_json('data/levels.json')
        if str(ctx.guild.id) not in levels: levels[str(ctx.guild.id)] = {}
        levels = levels[str(ctx.guild.id)]
        if str(user.id) not in levels: levels[str(user.id)] = {'xp': 0, 'lvl': 1}
        if user.bot: levels[str(user.id)] = {'xp': 88005553535, 'lvl': 228.1337}
        usr = levels[str(user.id)]
        img = Image.open('assets/img/level.png')
        d = ImageDraw.Draw(img)
        d.text((165, 30), ctx.l10n('lvl.level', lvl=usr['lvl']), font=self.font, fill=(255,255,255,255))
        d.text((165, 75), ctx.l10n('lvl.xp', xp=usr['xp'], xp_needed=usr['lvl']*10), font=self.font, fill=(255,255,255,255))
        avatar_size = (100, 100)
        mask = Image.new('L', avatar_size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + avatar_size, fill=255)
        response = requests.get(str(user.avatar_url_as(format='png')))
        avatar = Image.open(BytesIO(response.content))  
        avatar = avatar.resize(avatar_size, Image.ANTIALIAS)
        avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        avatar.putalpha(mask)
        img.paste(avatar, (30,43), avatar)
        if usr['xp'] > 0:
            frompos = (164, 120) 
            xpos = (usr['xp']/(usr['lvl']*10))*558+82
            if xpos < 164: xpos = 164
            if xpos > 559: xpos = 559
            topos = (xpos, 141)
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            progressbar = ImageDraw.Draw(overlay)
            progressbar.rectangle(frompos+topos, fill=(0,0,0,40))
            img = Image.alpha_composite(img, overlay)
            img = img.convert("RGB")
        byte = BytesIO()
        img.save(byte, 'PNG')
        byte.seek(0)
        await ctx.send(file=discord.File(byte, filename=f'{user.name}\'s card.png'))     

def setup(bot: Bot):
    bot.add_cog(Economy(bot))