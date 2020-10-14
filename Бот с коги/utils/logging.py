from discord.ext import commands
import discord, re
from lib.botclass import Bot
import lib.api, time
from datetime import datetime

class Logging(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.exc_debug['commands'].append(len(self.bot.exc_debug['commands'])+1)
        c = self.bot.load_json('data/command_uses.json')
        if ctx.command.qualified_name not in c: c[ctx.command.qualified_name] = 0
        c[ctx.command.qualified_name] += 1
        self.bot.write_json('data/command_uses.json', c)
        chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['other'])
        await chn.send(embed=discord.Embed(title=f'Выполнена команда `{ctx.command}`').add_field(name='Выполнена пользователем', value=f'{ctx.author.mention} | {ctx.display} ({ctx.author.id})') \
            .add_field(name='Выполнена в', value=f'{ctx.guild} > {ctx.channel}') \
            .add_field(name='Сообщение', value=ctx.message.clean_content, inline=False))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['guilds'])
        await chn.send(embed=discord.Embed(title='Меня добавили на сервер', description=f'Имя сервера: {guild.name}\nСервер создан: {str(guild.created_at)}\n\nТекстущее кол-во серверов: {len(self.bot.guilds)}', color=discord.Colour.green()).set_thumbnail(url=guild.icon_url))
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['guilds'])
        await chn.send(embed=discord.Embed(title='Меня убрали с сервера :(', description=f'Имя сервера: {guild.name}\nСервер создан: {str(guild.created_at)}\n\nТекстущее кол-во серверов: {len(self.bot.guilds)}', color=discord.Colour.red()).set_thumbnail(url=guild.icon_url))
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content: return
        
        if self.bot.http.token in after.clean_content or after.clean_content.find(self.bot.http.token) != -1:
            context = await self.bot.get_context(before)
            await context.send(":warning: :warning: :warning: My token was detected!")
            try:
                chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['errors'])
                await chn.send('@everyone :warning: :warning: :warning:', embed=discord.Embed(title='Обнаружен мой токен!', description=f'Обнаружен в: {after.guild} > {after.channel} | Отправлен {after.author} ({after.author.id})\n\nТокен был успешно перегенерирован через GitHub Gist.'))           
            except: pass
            return await context.invoke(self.bot.get_command('destroytoken'), token=self.bot.http.token)
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.http.token in message.clean_content or message.clean_content.find(self.bot.http.token) != -1:
            context = await self.bot.get_context(message)
            await context.send(":warning: :warning: :warning: My token was detected!")
            try:
                chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['errors'])
                await chn.send('@everyone :warning: :warning: :warning:', embed=discord.Embed(title='Обнаружен мой токен!', description=f'Обнаружен в: {message.guild} > {message.channel} | Отправлен {message.author} ({message.author.id})\n\nТокен был успешно перегенерирован через GitHub Gist.'))           
            except: pass
            return await context.invoke(self.bot.get_command('destroytoken'), token=self.bot.http.token)
        match = re.match(pattern=r'[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+', string=message.clean_content)
        if match:
            if message.guild and message.guild.id == 489764714549739521: return
            tokens = match.regs
            for reg in tokens:
                token = message.clean_content[reg[0]:reg[1]]
                if 'username' in (await lib.api.check_token(token)):
                    context = await self.bot.get_context(message)
                    await context.send("[Silentic Protection] :warning: Detected someone's token, destroying it...")
                    await context.invoke(self.bot.get_command('destroytoken'), token=token)
            return
        if message.channel.id == 714453768229355522:
            await message.add_reaction('👍')
            await message.add_reaction('👎')

def setup(bot: Bot):
    bot.add_cog(Logging(bot))