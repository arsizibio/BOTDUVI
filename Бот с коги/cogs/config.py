import discord, os, asyncio, traceback
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
import lib.errors as silentic_errors

class Config(commands.Cog):
    '''cogs.config.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.config.desc'
        self.thumbnail = 'utils'

    @commands.command(name='embedcolor', aliases=['embed_color', 'embedclr'])
    async def embedcolor(self, ctx, new_color = None):
        '''embedcolor.desc'''
        embedcolor = self.bot.load_json('data/embedcolor.json')
        if not new_color:
            if str(ctx.author.id) not in embedcolor: embedcolor[str(ctx.author.id)] = ctx.l10n('embedcolor.not_set')
            await ctx.send(embed=discord.Embed(title=ctx.l10n('embedcolor.yourcolor', color=embedcolor[str(ctx.author.id)])).set_footer(text=ctx.l10n('embedcolor.howTo')))
        else:
            try:
                if len(new_color) > 10: raise TypeError('invalidColor')
                embedcolor[str(ctx.author.id)] = new_color.replace('#', '')
                await ctx.send(embed=discord.Embed(title=ctx.l10n('embedcolor.changed'), color=discord.Color(int(new_color.replace('#', ''), 16))))
            except:
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("embedcolor.invalid")}')
            self.bot.write_json('data/embedcolor.json', embedcolor)

    @commands.command(name='language', aliases=['lang'])
    async def language(self, ctx, new_lang = None):
        '''language.desc'''
        langList = self.bot.load_json('data/locale.json')
        if not new_lang:
            await ctx.send(embed=discord.Embed(title=ctx.l10n('language.yourLang', language=ctx.l10n("language.name"))).set_footer(text=ctx.l10n('language.howTo')))
        else:
            new_lang = new_lang.lower()
            langs = [x for x in self.bot.locales]
            aliases = {}
            for langName in [x for x in self.bot.locales if 'language-info' in self.bot.locales[x]]:
                lang = self.bot.locales[langName]
                for alias in lang['language-info']['aliases']:
                    aliases[alias] = langName
                aliases[langName] = langName
            langFormatted = []
            for lang in langs:
                formatted = [lang]
                [formatted.append(x) for x in aliases if x != lang and aliases[x] == lang]
                formatted.sort(key=len)
                langFormatted.append('/'.join(formatted))
            all_languages = ', '.join(langFormatted)
            if [x for x in new_lang if x not in 'qwertyuiopasdfghjklzxcvbnm_'] != []:
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("language.unknownLang", language=new_lang, languageList=all_languages)}')
            if new_lang not in aliases:       
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("language.unknownLang", language=new_lang, languageList=all_languages)}')
            langList[ctx.user] = str(aliases[new_lang])
            self.bot.write_json('data/locale.json', langList)
            self.bot.load_locales()
            await asyncio.sleep(0.1)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("language.successful", language=ctx.l10n("language.name"))} ')
    @commands.group(name='prefix', invoke_without_command=True)
    async def prefix(self, ctx):
        '''prefix.desc'''
        prefixes = self.bot.load_json('data/prefixes.json')
        embed = discord.Embed()
        guildPrefix = ctx.l10n('prefix.not_set')
        selfPrefix = ctx.l10n('prefix.not_set')
        if str(ctx.author.id) in prefixes['self']: selfPrefix = prefixes['self'][str(ctx.author.id)]
        if str(ctx.guild.id) in prefixes['guild']: guildPrefix = prefixes['guild'][str(ctx.guild.id)]
        embed.add_field(name=ctx.l10n('prefix.self') + ' | ' + ctx.l10n('prefix.self.howTo'), value=selfPrefix, inline=False)
        embed.add_field(name=ctx.l10n('prefix.guild') + ' | ' + ctx.l10n('prefix.guild.howTo'), value=guildPrefix)
        embed.set_footer(text=ctx.l10n('prefix.howToReset'))
        await ctx.send(embed=embed)
    @prefix.command(name='self')
    async def selfprefix(self, ctx, prefix):
        '''prefix.self'''
        prefixes = self.bot.load_json('data/prefixes.json')
        if prefix == 'reset':
            del prefixes['self'][str(ctx.author.id)]
            self.bot.write_json('data/prefixes.json', prefixes)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("prefix.set.reset", type=ctx.l10n("prefix.type.self"))}')
        else:
            prefixes['self'][str(ctx.author.id)] = prefix
            self.bot.write_json('data/prefixes.json', prefixes)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("prefix.set.ok", prefix=prefix, type=ctx.l10n("prefix.type.self"))}')
    @prefix.command(name='guild')
    @commands.has_permissions(manage_guild=True)
    async def guildprefix(self, ctx, prefix):
        '''prefix.guild'''
        prefixes = self.bot.load_json('data/prefixes.json')
        if prefix == 'reset':
            del prefixes['guild'][str(ctx.guild.id)]
            self.bot.write_json('data/prefixes.json', prefixes)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("prefix.set.reset", type=ctx.l10n("prefix.type.guild"))}')
        else:
            prefixes['guild'][str(ctx.guild.id)] = prefix
            self.bot.write_json('data/prefixes.json', prefixes)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("prefix.set.ok", prefix=prefix, type=ctx.l10n("prefix.type.guild"))}')

    @commands.group(name='rule', invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def rule(self, ctx):
        '''none'''
        await ctx.call_help()
    @rule.command(name='allow-credit')
    @commands.has_permissions(manage_guild=True)
    async def allow_credit(self, ctx, toggle: bool = None):
        '''rule.credit.desc'''
        rules = self.bot.load_json('data/rules.json')
        if toggle == None:
            if str(ctx.guild.id) not in rules['credit']: enabled = True
            else: enabled = rules['credit'][str(ctx.guild.id)]
            if enabled: await ctx.send(embed=discord.Embed(title=ctx.l10n('rule.credit.enabled')).set_footer(text=ctx.l10n('rule.credit.enabled.howTo')))
            else: await ctx.send(embed=discord.Embed(title=ctx.l10n('rule.credit.disabled')).set_footer(text=ctx.l10n('rule.credit.disabled.howTo')))
        else:
            if toggle == False: 
                rules['credit'][str(ctx.guild.id)] = False
                self.bot.write_json('data/rules.json', rules)
                await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("rule.credit.disabled")} ')
            else:
                rules['credit'][str(ctx.guild.id)] = True
                self.bot.write_json('data/rules.json', rules)
                await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("rule.credit.enabled")} ')

    @rule.command(name='enable-leveling', aliases=['enable-lvl'])
    @commands.has_permissions(manage_guild=True)
    async def leveling_toggle(self, ctx, toggle: bool = None):
        '''rule.lvl.desc'''
        lvl = self.bot.load_json('data/lvl_enabled.json')
        if toggle == None:
            if str(ctx.guild.id) not in lvl: enabled = False
            else: enabled = lvl[str(ctx.guild.id)]
            if enabled: await ctx.send(embed=discord.Embed(title=ctx.l10n('rule.lvl.enabled')).set_footer(text=ctx.l10n('rule.lvl.enabled.howTo')))
            else: await ctx.send(embed=discord.Embed(title=ctx.l10n('rule.lvl.disabled')).set_footer(text=ctx.l10n('rule.lvl.disabled.howTo')))
        else:
            if toggle == False:
                lvl[str(ctx.guild.id)] = False
                self.bot.write_json('data/lvl_enabled.json', lvl)
                await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("rule.lvl.disabled")} ')
            else:
                lvl[str(ctx.guild.id)] = True
                self.bot.write_json('data/lvl_enabled.json', lvl)
                await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("rule.lvl.enabled")} ')
    
    @rule.command(name='cooldown')
    @commands.has_permissions(manage_guild=True)
    async def cooldown_rule(self, ctx, command = None, seconds: int = None):
        '''rule.cooldown.desc'''
        rule = self.bot.load_json('data/rules.json')
        if not seconds and command:
            return await ctx.call_help()
        if command and command not in rule['cooldown']: command = None
        if not command:
            embed = discord.Embed(title=ctx.l10n('rule.cooldown.list'))
            for cmd in rule['cooldown']:
                cooldown = ctx.l10n('rule.cooldown.notSet')
                if str(ctx.guild.id) in rule['cooldown'][cmd]:
                    cooldown = rule['cooldown'][cmd][str(ctx.guild.id)]
                embed.add_field(name=cmd, value=str(cooldown))
            embed.set_footer(text=ctx.l10n('rule.cooldown.tip'))
            await ctx.send(embed=embed)
        else:
            rule['cooldown'][command][str(ctx.guild.id)] = seconds
            self.bot.write_json('data/rules.json', rule)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("rule.cooldown.ok", command=command, sec=seconds)}')
def setup(bot: Bot):
    bot.add_cog(Config(bot))