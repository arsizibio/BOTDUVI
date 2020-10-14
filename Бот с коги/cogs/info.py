import discord
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
import lib.errors as silentic_errors

class Information(commands.Cog):
    '''cogs.info.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.info.desc'
        self.thumbnail = 'info'

    @commands.command(name='help', aliases=['?', 'commands'])
    async def help_command(self, ctx: Context, *, command = None):
        '''help.desc'''
        if not command:
            pag = Paginator(ctx)
            for cogName in self.bot.cogs:
                cog = self.bot.cogs[cogName]
                if not str(cog.__module__).startswith('cogs.'):
                    continue
                cogDesc = getattr(cog, 'desc', None)
                if cogDesc:
                    cogDesc = ctx.l10n(cogDesc)
                embed = discord.Embed(title=ctx.l10n(cog.__doc__), description=cogDesc)
                commandList = [f'``{self.bot.formatCommandName(x)}``' for x in self.bot.commands if str(x.cog_name) == str(cogName) and not x.hidden]
                if len(commandList) == 0: continue
                embed.add_field(name=ctx.l10n('help.cog.commands'), value=', '.join(commandList), inline=False)
                thumbnail = getattr(cog, 'thumbnail', None)
                if thumbnail:
                    embed.set_thumbnail(url=self.bot.icon(f'cog_{thumbnail}').url)
                pag.add_page(embed)
            await pag.paginate()
        else:
            cmd = self.bot.get_command(command)
            if not cmd:
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("help.commandNotFound", command=command)}')
            else:
                if not str(cmd.module).startswith('cogs.'):
                    return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("help.commandNotFound", command=command)}')
                embed = discord.Embed(title=f'{cmd.qualified_name} {cmd.signature}', description=ctx.l10n(str(cmd.help)))
                if hasattr(cmd, 'commands'):
                    commandList = [f'``{self.bot.formatCommandName(x)}``' for x in cmd.commands if not x.hidden]
                    if len(commandList) == 0: commandList = [ctx.l10n('help.nothing')] 
                    embed.add_field(name=ctx.l10n('help.command.subcommands'), value=', '.join(commandList))
                await ctx.send(embed=embed)

    @commands.command(name='credits')
    async def credits(self, ctx):
        '''credits.desc'''
        embed = discord.Embed(title=ctx.l10n('credits.desc'))
        embed.add_field(name=ctx.l10n('credits.developers'), value=str(await self.bot.fetch_user(319050081795964928)), inline=False)
        embed.add_field(name=ctx.l10n('credits.hosters'), value=str(await self.bot.fetch_user(407524032292847624)), inline=False)
        embed.add_field(name=ctx.l10n('credits.translators'), value=', '.join([str(await self.bot.fetch_user(x)) for x in self.bot.load_json('data/translators.json')]), inline=False)
        embed.set_thumbnail(url=self.bot.icon('leaderboard').url)
        await ctx.send(embed=embed)
def setup(bot: Bot):
    bot.add_cog(Information(bot))