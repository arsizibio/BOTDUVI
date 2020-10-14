import discord, os, asyncio, requests, time
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
from io import BytesIO
import lib.errors as silentic_errors

class Moderation(commands.Cog):
    '''cogs.mod.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.mod.desc'
        self.thumbnail = 'mod'

    @commands.command(name='warn-config', aliases=['warn_config', 'warnconfig'])
    @commands.has_permissions(manage_guild=True, manage_roles=True)
    async def warnConfig(self, ctx, warnId: int = None, action: str = None):
        '''mod.warnconfig.desc'''
        warnconfig = self.bot.load_json('data/warnconfig.json')
        if str(ctx.guild.id) not in warnconfig:
            warnconfig[str(ctx.guild.id)] = {str(x+1): 'none' for x in range(10)}
        if not warnId and not action:
            embed = discord.Embed(title=ctx.l10n('mod.warnconfig.action_list'))
            actions = []
            for action in warnconfig[str(ctx.guild.id)]:
                astr = ctx.l10n("mod.warnconfig.warnId", id=action)
                if warnconfig[str(ctx.guild.id)][action] == 'none':
                    astr += ctx.l10n('mod.warnconfig.action.not_set')
                else:
                    astr += ctx.l10n(f'mod.warnconfig.action.{warnconfig[str(ctx.guild.id)][action]}')
                actions.append(astr)
            embed.description = '\n'.join(actions)
            await ctx.send(embed=embed)
        elif action not in ['mute', 'kick', 'ban', 'none']:
            await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("mod.warnconfig.incorrect_action")}')
        elif warnId < 1 or warnId > 10:
            await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("mod.warnconfig.incorrect_id")}')
        else:
            warnconfig[str(ctx.guild.id)][str(warnId)] = action
            self.bot.write_json('data/warnconfig.json', warnconfig)
            atl = ctx.l10n(f'mod.warnconfig.action.{action}')
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("mod.warnconfig.set", action=atl, id=warnId)}')

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        '''mod.warn.desc'''
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("mod.warn.fail")}')
        warns = self.bot.load_json("data/warns.json")
        warnconfig = self.bot.load_json('data/warnconfig.json')
        if str(ctx.guild.id) not in warns: warns[str(ctx.guild.id)] = {}
        if str(member.id) not in warns: warns[str(ctx.guild.id)][str(member.id)] = []
        warnId = len(warns[str(ctx.guild.id)][str(member.id)])
        if warnId >= 10:
            return await ctx.send(ctx.l10n('mod.warn.limit_reached', user=str(member)))
        warns[str(ctx.guild.id)][str(member.id)].append({'reason': str(reason), 'moderator': ctx.author.id, 'timestamp': time.time()})
        if warnconfig[str(ctx.guild.id)][str(warnId)] != 'none':
            action = warnconfig[str(ctx.guild.id)][str(warnId)]
            if action == 'mute':
                pass
            elif action == 'kick':
                pass
def setup(bot: Bot):
    bot.add_cog(Moderation(bot))