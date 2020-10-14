from discord.ext import commands
import discord, re
from lib.botclass import Bot
import lib.api

class AdminCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def cog_check(self, ctx):
        if ctx.author.id not in self.bot.config['owners']:
            raise commands.NotOwner('Not owner')
        return True
    
    @commands.command(name='acceptidea', aliases=['accept-idea'], hidden=True)
    async def acceptSuggest(self, ctx, msgId: int, *, description):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['suggest'])
        msg = await chn.fetch_message(msgId)
        embed = msg.embeds[0]
        try: embed.remove_field(0)
        except: pass
        embed.add_field(name=f'Ответ от разработчика ({ctx.display})', value=description)
        embed.color = discord.Colour.green()
        await msg.edit(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='declineidea', aliases=['decline-idea'], hidden=True)
    async def declineSuggest(self, ctx, msgId: int, *, description):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['suggest'])
        msg = await chn.fetch_message(msgId)
        embed = msg.embeds[0]
        try: embed.remove_field(0)
        except: pass
        embed.add_field(name=f'Ответ от разработчика ({ctx.display})', value=description)
        embed.color = discord.Colour.red()
        await msg.edit(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='commentidea', aliases=['comment-idea'], hidden=True)
    async def commentSuggest(self, ctx, msgId: int, *, description):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['suggest'])
        msg = await chn.fetch_message(msgId)
        embed = msg.embeds[0]
        try: embed.remove_field(0)
        except: pass
        embed.add_field(name=f'Ответ от разработчика ({ctx.display})', value=description)
        embed.color = discord.Colour.dark_grey()
        await msg.edit(embed=embed)
        await ctx.message.delete()

    @commands.command(name='bestuses')
    async def bestuses(self, ctx):
        c = self.bot.load_json('data/command_uses.json')
        uses = sorted(c, key=lambda x : c[x], reverse=True)
        desc = []
        for use in uses:
            desc.append(f'{use}: {c[use]}')
        await ctx.send(embed=discord.Embed(description='```yaml\n' + '\n'.join(desc) + '\n```'))

    @commands.command(name='commanduses')
    async def commanduses(self, ctx, command):
        c = self.bot.load_json('data/command_uses.json')
        if command not in c: return await ctx.send(f'Cloudn\'t find command {command}')
        await ctx.send(f'Command {command} has {c[command]} uses')

    @commands.command(name='adminhelp', aliases=['admin-help'])
    async def admhelp(self, ctx):
        await ctx.send(', '.join(x.name for x in self.bot.commands if x.cog_name == 'AdminCommands'))

def setup(bot: Bot):
    bot.add_cog(AdminCommands(bot))