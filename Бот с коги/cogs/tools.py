import discord, os, asyncio, requests
from discord.ext import commands
from lib.botclass import Bot
from lib.context import SilenticContext as Context
from lib.paginator import Paginator
from io import BytesIO
import lib.errors as silentic_errors
import lib.api
import random, json, aiohttp

class Tools(commands.Cog): 
    '''cogs.tools.doc'''
    def __init__(self, bot: Bot):
        self.bot = bot
        self.desc = 'cogs.tools.desc'
        self.thumbnail = 'utils'

    @commands.command(name='destroy-token', aliases=['destroy_token', 'destroytoken'])
    async def destroytoken(self, ctx, token):
        '''destroytoken.desc'''
        bot_data = await lib.api.check_token(token)
        if 'username' not in bot_data:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("destroytoken.unknown")}')
        id_ = await lib.api.create_gist(f'This GIST published automatically from bot {str(self.bot.user)} to prevent using token in token.txt by third-party users. Discord will automatically regenerate this token.', files={'token.txt': {'content': f'{token} | Destroyed with command "destroytoken" by user {ctx.display} ({ctx.author.id})'}})
        await lib.api.delete_gist(id_)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("destroytoken.ok", username=bot_data["username"])}')

    @commands.command(name='suggest')
    async def suggest(self, ctx, *, idea):
        '''suggest.desc'''
        await ctx.send(embed=discord.Embed(title=ctx.l10n('suggest.sent'), description=ctx.l10n('suggest.sent.desc')))
        chn = await self.bot.fetch_channel(self.bot.config['channels']['suggest'])
        msg = await chn.send(embed=discord.Embed(description=idea).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


    @commands.command(name='botinfo', aliases=['bot-info', 'bot_info'])
    async def botinfo(self, ctx, botId: int):
        '''botinfo.desc'''
        msg = await ctx.send(f'{self.bot.icon("processing")} | {ctx.l10n("botinfo.loading")}')
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v6/oauth2/authorize?client_id={botId}&scope=bot',
                headers={'Authorization': self.bot.secret['selfbottoken']}) as resp:
                    data = await resp.json()
        if 'message' in data and data['message'] == 'Unknown Application':
            return await msg.edit(content=f'{self.bot.icon("error")} | {ctx.l10n("botinfo.unknown")}')
        embed = discord.Embed()
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/' + str(data['bot']['id']) + '/' + data['bot']['avatar'])
        app_info = []
        app_info.append(f'{ctx.l10n("botinfo.application.name")}: {data["application"]["name"]}')
        app_info.append(f'{ctx.l10n("botinfo.application.summary")}: ```{data["application"]["summary"]}```')
        embed.add_field(name=ctx.l10n('botinfo.application'), value='\n'.join(app_info), inline=False)
        bot_info = []
        bot_info.append(f'{ctx.l10n("botinfo.bot.public")}: {data["application"]["bot_public"]}')
        bot_info.append(f'{ctx.l10n("botinfo.bot.require_code_grant")}: {data["application"]["bot_require_code_grant"]}')
        bot_info.append(f'{ctx.l10n("botinfo.bot.name")}: {data["bot"]["username"]}#{data["bot"]["discriminator"]} | {data["bot"]["id"]}')
        bot_info.append(f'{ctx.l10n("botinfo.bot.guild_count")}: {data["bot"]["approximate_guild_count"]}')
        embed.add_field(name=ctx.l10n('botinfo.bot'), value='\n'.join(bot_info), inline=False)
        await msg.edit(content=None, embed=embed)

    @commands.group(name='bottranslate', aliases=['bottl'], invoke_without_command=True)
    async def bottl(self, ctx):
        '''bottl.desc'''
        await ctx.call_help()
    @bottl.command(name='add-dashboard', aliases=['dashboard', 'add-db'], hidden=True)
    @commands.is_owner()
    async def btldashboard(self, ctx, *, text):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['tl-dashboard'])
        await chn.send('<@&715167135781093406>', embed=discord.Embed(title=f'Уведомление', description=text))
    @bottl.command(name='format')
    async def btlformat(self, ctx, lang, string, *, jsonData = '{}'):
        '''bottl.format.desc'''
        if lang not in self.bot.locales: return await ctx.send(f'unknown language - {lang}')
        if string not in self.bot.locales[lang]: return await ctx.send(f'unknown string - [{lang}:{string}]')
        try:
            data = json.loads(jsonData)
        except Exception as e:
            return await ctx.send(f'Error in JSON: {e}')
        if type(data) != dict:
            return await ctx.send(f'Error in JSON: Requred dict, not {type(data).__name__}')
        await ctx.send(str(ctx.l10n_lang(lang, string, **data))[:2000])
    @bottl.command(name='bug')
    async def btlbug(self, ctx, lang, *, bug):
        '''bottl.bug.desc'''
        chn = await self.bot.fetch_channel(self.bot.config['channels']['tl-bugs'])
        await chn.send(embed = discord.Embed(title=f'Обнаружена ошибка с переводом') \
                               .add_field(name='Язык', value=lang, inline=False) \
                               .add_field(name='Описание бага', value=bug, inline=False))
    @bottl.command(name='submit') 
    async def btlsubmit(self, ctx, *, text = None): 
        '''bottl.submit.desc'''
        if len(ctx.message.attachments) == 0:
            return await ctx.call_help()
        tl = self.bot.load_json('data/translators.json')
        if ctx.author.id in tl:
            await ctx.message.attachments[0].save(f'locale/{ctx.message.attachments[0].filename}')
            chn = await self.bot.fetch_channel(self.bot.config['channels']['tl-logs'])
            commit = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm12345567890') for _ in range(10))
            await chn.send(embed=discord.Embed(title=f'commit-{ctx.message.attachments[0].filename.split(".")[0]}:{commit}', description=text), file=discord.File(f'locale/{ctx.message.attachments[0].filename}', filename=f'{commit}.yaml'))
            self.bot.load_locales()
            return await ctx.send('OK')
        u = await self.bot.fetch_user(319050081795964928)
        content = requests.get(ctx.message.attachments[0].url).content
        byte = BytesIO(content)
        byte.seek(0)
        await u.send(f'Bot translation request\nFrom {ctx.display} ({ctx.user})', file=discord.File(fp=byte, filename=f'{ctx.message.attachments[0].filename}'))
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("bottl.submit.ok")}')
    @bottl.command(name='get')
    async def btlget(self, ctx, lang):
        '''bottl.get.desc'''
        langs = [x.name.split('.')[0] for x in os.scandir('locale') if x.name.endswith('.yaml')]
        all_languages = ', '.join(langs)
        if [x for x in lang if x not in 'qwertyuiopasdfghjklzxcvbnm_'] != []:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("language.unknownLang", language=lang, languageList=all_languages)}')
        if lang not in langs:       
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("language.unknownLang", language=lang, languageList=all_languages)}')
        await ctx.send(file=discord.File(fp=f'locale/{lang}.yaml', filename=f'{lang}.yaml'))

def setup(bot: Bot):
    bot.add_cog(Tools(bot))