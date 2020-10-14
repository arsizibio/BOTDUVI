import sqlite3
import traceback
import sys
from discord.ext import commands
import discord
import humanize
import random, asyncio, aiohttp
import datetime
from datetime import datetime as dt
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
humanize.i18n.activate('ru_RU')
from pyowm import OWM
from discord.ext import commands
from colorama import Fore, init, Style
import asyncio
import random   
import json
import datetime 
import timedelta
import psutil as ps
from Cybernator import Paginator
import clock
import platform
import pymongo
import datetime
import pyowm



client = commands.Bot(command_prefix = 'D.' )

client.remove_command('help')

#events
@client.event
async def on_guild_join(guild):
    print(f'''
{Fore.YELLOW}
==============================================
{Style.RESET_ALL}
[GUILD]   Бот присоединился к серверу!
[GUILD]   Информация о сервере
{Fore.YELLOW}
==============================================
{Style.RESET_ALL}
[GUILD]  Сервер           - {guild.name}
[GUILD]  Владелец сервера - {guild.owner}
[GUILD]  ID бота          - {guild.id}
{Fore.YELLOW}
==============================================
{Style.RESET_ALL}
    ''')
    embed = discord.Embed(title='Duvi', description=f"Добрый день!\n\n Вы получили это сообщение т.к на ваш сервер {guild.name} был добавлен Duvi Бот.\nЭто чисто информативное сообщение, сделанное для того, чтобы вы знали немного больше о том, чем пользуетесь.", color=0x800080)
    embed.add_field( name="Полезная информация:", value=f"Он очень многое умеет что бы это узнать напишите D.help Удачи наш сайт:https://arsizi.github.io/")
    embed.set_footer(text='Duvi', icon_url=client.user.avatar_url)

    await guild.owner.send(embed=embed)

    getChannel = client.get_channel(703653241027821658)

    j_e = discord.Embed(title=f"Бот присоединился к серверу {guild.name}",description=f"Информация о сервере:\n\nСервер - {guild.name}\nID сервера - {guild.id}\nВладелец сервера - {guild.owner}", color=0x800080)

    await getChannel.send(embed=j_e)

#commands
@client.command()
async def commmand_name(args):
    pass


# %help




@client.event
async def on_ready():
    print('БОТ ЗАПУСТИЛСЯ by ars izi')

@client.command(pass_context=True)
@commands.has_permissions( administrator = True )
async def dmall(ctx, message=None):
    await ctx.message.delete()
    if message != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(message)
                print("'" + message + "' Отправлено к:" + member.name)

            except:
                print("Не могу отправит: '"+ message + "' к: " + member.name)
    else:
        ctx.send("Ты забыл написать сообщение!")

@client.command()
async def vistrelit( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    embed = discord.Embed(title = 'Выстрел', description = 'Вы сможете в кого-то выстрелить.', colour = discord.Color.red())

    embed.add_field( name = '**Доставание дробовика**', value = f"{ctx.author.mention} достаёт дробовик...", inline = False )

    await asyncio.sleep( 3 )
    embed.add_field( name = '**Направление дробовика**', value = f"{ctx.author.mention} направляет дробовик на {member.mention}...", inline = False )

    await asyncio.sleep( 2 )
    embed.add_field( name = '**Стрельба**', value = f"{ctx.author.mention} стреляет в {member.mention}...", inline = False )

    embed.set_image(url='https://media.discordapp.net/attachments/690222948283580435/701494203607416943/tenor_3.gif')

    await asyncio.sleep( 2 )
    embed.add_field( name = '**Кровь**', value = f"{member.mention} истекает кровью...", inline = False )

    await ctx.send( embed = embed )

bad_words = ('Код не работает','Сделайте за меня','Вы обязаны мне помогать','что делать','я не хочу гуглить','исходник бота не работает','Твой бот не работает','Как')

@client.event
async def on_message(message):
    for words in bad_words:
        if words in message.content.lower():
            await message.delete()
            await message.channel.send('Ну это бан')

#connect

import traceback
import sys
from discord.ext import commands
import discord
import humanize
import random, asyncio, aiohttp
import datetime
from datetime import datetime as dt
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
humanize.i18n.activate('ru_RU')


# errors 

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
         await ctx.send("***Данной команды нету или ты неправильно написал***")


bad_words = ['Твой бот нерабочий','У тебя плохой бот']#cуда сообщения плохие

@client.event
async def on_message (message):
  await client.process_commands(message)
  mes = message.content.lower()#регистр
  for i in bad_words:#цикл
    if i in mes:
      await message.delete()
      msg = await message.channel.send(f'{message.author.mention} Ну это бан')#тут ваш текст который будет писаться в чат и исчезнет через время указывать в asyncio.sleep()
      await asyncio.sleep(3)#3 секунды и убираем сообщение
      await msg.delete()        
      сhannel = client.get_channel(703653241027821658)
      emb = discord.Embed(title = 'Нарушение:', colour = discord.Color.red())#дальше сами логи тут уже ваша фантазия
      emb.add_field(name = 'Имя:', value = f'{message.author.name}', inline=False) #
      emb.add_field(name = 'Причина:', value = f'Не правильно({mes})')
      emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
      emb.set_footer(text = 'Спасибо за использования нашего бота')

      await ctx.send(embed = emb) #вывод embed 


@client.command(aliases=['Say', 'Сказать', 'сказать', 'Скажи', 'скажи', 'SAY', 'СКАЗАТЬ', 'СКАЖИ', 'Вывести', 'вывести', 'ВЫВЕСТИ', 'Выведи', 'выведи', 'ВЫВЕДИ'])
@commands.has_permissions(administrator=True)
async def say(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=discord.Embed(title="Не бузи!", description=f":x: {ctx.author.mention}, укажи сообщение, которое хочешь отправить от именни бота :x:", color=0xFF0000))
    else:
        await ctx.message.delete()
        embed = discord.Embed(description=f'{arg}', color=0xa43dd8)
        embed.set_footer(text=f'{client.user.name} © 2030 | Все права защищены', icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)

        print(f'[log Command] Была исользована команда - >say. Использовал - Администратор: {ctx.author}\n')

def bytes2human(number, typer=None):
    # >> bytes2human(10000)
    # >> '9.8K'
    # >> bytes2human(100001221)
    # >> '95.4M'

    if typer == "system":
        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')  # Для перевода в Килобайты, Мегабайты, Гигобайты, Террабайты, Петабайты, Петабайты, Эксабайты, Зеттабайты, Йоттабайты
    else:
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # Для перевода в обычные цифры (10k, 10MM)

    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if number >= prefix[s]:
            value = float(number) / prefix[s]
            return '%.1f%s' % (value, s)

    return f"{number}B"

@say.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        e = discord.Embed(title='Не бузи!', color = 0xFF0000)
        e.description = f':x: {ctx.author.mention}, у тебя нет прав, что-бы использовать эту команду! :x:'
        await ctx.send(embed=e)
    else:
        raise error

    @commands.command(name='level')
    async def level_cmd(self, ctx, user: discord.Member = None):
        if not user: user = ctx.author
        if user.client: return await ctx.send(embed=discord.Embed(description=f'Боты не могут иметь уровень', color=discord.Colour.red()).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url).set_footer(text=f'{self.bot.prefix}{ctx.command} {ctx.command.signature}'))
    
        levels = await self.client.read_json('levels.json')
        if str(user.id) not in levels: levels[str(user.id)] = {'messages': 0, 'xp': 0, 'level': 1}
        usr = levels[str(user.id)]

        img = Image.open('level.png')
        d = ImageDraw.Draw(img)
        d.text((315, 47), str(usr['level']), font=self.font, fill=(255,255,255,255))
        d.text((215, 88), str(usr['xp']) + '/' + str(usr['level']*10), font=self.font, fill=(255,255,255,70))


        avatar_size = (100, 100)
        mask = Image.new('L', avatar_size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + avatar_size, fill=255)

        response = requests.get(str(user.avatar_url_as(format='png')))
        avatar = Image.open(BytesIO(response.content))
        avatar = avatar.resize(size=avatar_size)
        avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        avatar.putalpha(mask)

        # alpha = avatar.convert('RGBA').split()[-1]
        # avatar_b = Image.new("RGBA", avatar.size, (9,10,11,255))
        # avatar_b.paste(avatar, mask=alpha)
        # avatar = avatar_b
        img.paste(avatar, (30,43), avatar)
        
        if usr['xp'] > 0:
            frompos = (164, 119) 
            xpos = (usr['xp']/(usr['level']*10))*558+82
            if xpos < 164: xpos = 164
            if xpos > 559: xpos = 559
            topos = (xpos, 143)
            progressbar = ImageDraw.Draw(img)
            progressbar.rectangle(frompos+topos, fill=(52,152,219))

        byte = BytesIO()
        img.save(byte, 'PNG')
        byte.seek(0)
        await ctx.send(file=discord.File(byte, filename=f'{user.name}\'s card.png'))
        await self.bot.write_json('levels.json', levels)

@client.command(name='weather', aliases=['погода'])
async def weather(ctx, city: str = None):
    if not city:
        await ctx.send(embed = discord.Embed(description="**Ты не указал город -_-**", colour=discord.Color.from_rgb(47, 49, 54)))
        await ctx.message.add_reaction("🔴")
    else:
        owm = pyowm.OWM('64d8187cd475780284532f9b0d36ba0d')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        temp_max = w.temperature('celsius')["temp_max"]
        temp_min = w.temperature('celsius')["temp_min"]
        feels_like = w.temperature('celsius')["feels_like"]

        embed = discord.Embed(
            colour=discord.Color.from_rgb(47, 49, 54),
            description=f"**Погода в городе {city}**",
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url="https://avatars.mds.yandex.net/get-pdb/752643/d215f5fe-77ec-4923-aea7-b2184f2b6598/orig")
        embed.add_field(name="Температура", value=f"{temp} °С")
        embed.add_field(name="Ощущается как", value=f"{feels_like} °С")
        embed.add_field(name="Максимальная температура", value=f"{temp_max} °С")
        embed.add_field(name="Минимальная температура", value=f"{temp} °С")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("🟢")

@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(embed = discord.Embed(
            colour=discord.Color.from_rgb(47, 49, 54),
            description=f"**Город не найден**"
        ))
        await ctx.message.add_reaction("🔴")

import discord, subprocess, sys, time, os, colorama, base64, codecs, datetime, io, random, numpy, datetime, smtplib, string, ctypes
import urllib.parse, urllib.request, re, json, requests, webbrowser, aiohttp, dns.name, asyncio, functools, logging

from discord.ext import (
    commands,
    tasks
)
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlencode
from pymongo import MongoClient
from selenium import webdriver
from threading import Thread
from subprocess import call
from itertools import cycle
from colorama import Fore
from sys import platform
from PIL import Image
import pyPrivnote as pn
from gtts import gTTS


@client.command()
async def hug(ctx, user: discord.Member): # b'\xfc'
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    em = discord.Embed(description=user.mention)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def smug(ctx, user: discord.Member): # b'\xfc'
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/smug")
    res = r.json()
    em = discord.Embed(description=user.mention)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def pat(ctx, user: discord.Member): # b'\xfc'
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    em = discord.Embed(description=user.mention)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def kiss(ctx, user: discord.Member): # b'\xfc'
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    em = discord.Embed(description=user.mention)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)


slap = '[{prefix}slap участник'

popygai = '[{prefix}popygai слово'

feedback = '[{perefix} feedback отзыв]'

prefix = 'D.' #префикс сам поставишь

admin = 'Администрации' #если нужно поменяешь

clear = f'[{prefix}clear кол-во сообщений]'

ban = f'[{prefix}ban @участник]'

coin = f'[{prefix}coin]'

dmall = f'[{prefix}dmall сообщение]'

hug = f'[{prefix}hug @участник]'

kick = f'[{prefix}kick @участник, причина]'

Vistrel = f'[{prefix}Vistrelit @участник]'

mute = f'[{prefix}mute @участник, промежуток времени, причина]'

kiss = f'[{prefix}kiss @участник,]'

say = f'[{prefix}say сообщение]'

serverinfo = f'[{prefix}serverinfo]'

stats = f'[{prefix}stats]'

userinfo = f'[{prefix}userinfo @участник]'

unmute = f'[{prefix}unmute @участник]'

weather = f'[{prefix}weather город]'

@client.command()
async def help(ctx):
	emb = discord.Embed(title = 'Команды **бота**', description = f'{ctx.author.mention}, напиши их, увидишь **магию** :man_mage:', color = 0xFF7F50)
	emb.add_field(name = f'**`{prefix}clear`**', value = f'**Очистим чат** от **мусора**! Очистить чат от сообщений.\n - {clear} - **Только для {admin}**', inline = False)
	emb.add_field(name = f'**`{prefix}weather`**', value = f'**Это погода**! Эта команда скажет какая погода в городе.\n - {weather} ', inline = False)
	emb.add_field(name = f'**`{prefix}ban`**', value = f'Ты не пройдешь! **Забанить** участника - {ban}', inline = False)
	emb.add_field(name = f'**`{prefix}coin`**', value = f'Орел и решка! **Игра** - **орел и решка** - {coin}', inline = False)
	emb.add_field(name = f'**`{prefix}dmall`**', value = f'Вам **поссылка**, господин - Отправить **сообщение** всем **участникам**\n - {dmall} - **Только для {admin}**', inline = False)
	emb.add_field(name = f'**`{prefix}hug`**', value = f'Обнимашки! - Обнять **участника** - {hug}', inline = False)
	emb.add_field(name = f'**`{prefix}kick`**', value = f'Иди отсюдово! - Кикнуть **участника** с **сервера**\n - {kick} - **Только для {admin}**', inline = False)
	emb.add_field(name = f'**`{prefix}vistrelit`**', value = f'Выстрелить - "Выстрелить" в **участника** - {Vistrel}', inline = False)
	emb.add_field(name = f'**`{prefix}mute`**', value = f'Не говори,ты  - Замутить **участника**\n - {mute}\n - **Только для {admin}**', inline = False)
	emb.add_field(name = f'**`{prefix}say`**', value = f'Бип-Буп - Вывести **сообщение** в **чат** от именни **бота**\n - {say} - **Только для {admin}** ', inline = False)
	emb.add_field(name = f'**`{prefix}serverinfo`**', value = f'Инфиримиция - **Информация** о **сервере** - {serverinfo}', inline = False)
	emb.add_field(name = f'**`{prefix}info`**', value = f'Че по-чем, ботяра - **Информация** о **боте**', inline = False)
	emb.add_field(name = f'**`{prefix}unmute`**', value = f'Можешь сново говорить, - Размутить **участника**\n - {unmute} - **Только для {admin}**', inline = False)
	emb.add_field(name = f'**`{prefix}userinfo`**', value = f'Ты кто по жизни? - **Информация** об **участнике**\n - {userinfo}')
	emb.set_footer(text = f'{client.user.name} © 2030 | Все права защищены', icon_url = client.user.avatar_url)

	await ctx.author.send(embed = emb)




init()

@client.command()
async def slap( ctx, member: discord.Member ):


    embed = discord.Embed(title = 'Пощёчина ', description = 'Вы сможете дать пощёчину', colour = discord.Color.red())

    embed.add_field( name = '**Доставание Рук**', value = f"{ctx.author.mention} достаёт руки...", inline = False )

    
    embed.add_field( name = '**Ударяет **', value = f"{ctx.author.mention} Ударяет {member.mention}...", inline = False )

    embed.set_image(url='https://media.tenor.com/images/42c88f504736a31d6c2e649328d1ff3c/tenor.gif')

    await ctx.send( embed = embed )

@client.command()
async def covide(self, ctx, country=None):
        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == country:
                emb = discord.Embed()
                emb.add_field(name=f'Выздоровело:', value=f'{item["recovered"]} человек')
                emb.add_field(name=f'Заболеваний:', value=f'{item["cases"]} человек')
                emb.add_field(name=f'Погибло:', value=f'{item["deaths"]} человек')
                emb.add_field(name=f'Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                emb.add_field(name=f'Погибло за сутки:', value=f'+{item["todayDeaths"]} человек')
                emb.add_field(name=f'Проведено тестов:', value=f'{item["tests"]} человек')
                emb.add_field(name=f'Активные зараженные:', value=f'{item["active"]} человек')
                emb.add_field(name=f'В тяжелом состоянии:', value=f'{item["critical"]}  человек')
                emb.set_thumbnail(url=item["countryInfo"]['flag'])
                await ctx.send(embed=emb)


@client.command()
async def coin(ctx):
    choices = ['орел', 'решка', 'монетка упала ребром']
    color = discord.Color.green()
    emb = discord.Embed(color=color, title='Подбрасывание:', description=random.choice(choices))
    await ctx.send(embed=emb)

@client.command()
async def serverinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали {guild.created_at.strftime('%b %#d, %Y')}\n\n"
                                                             f"Регион {guild.region}\n\nГлава сервера {guild.owner}\n\n"
                                                             f"Людей и ботов на сервере {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)


# userinfo
@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

#фильтр сообщения
bad_words = ['сука', 'блять','еблан','заебись','нахуй','бля','пидр']#cуда сообщения плохие

@client.event
async def on_message (message):
  await client.process_commands(message)
  mes = message.content.lower()#регистр
  for i in bad_words:#цикл
    if i in mes:
      await message.delete()
      msg = await message.channel.send(f'{message.author.mention} ваше сообщение удалено. Причина: Мат')#тут ваш текст который будет писаться в чат и исчезнет через время указывать в asyncio.sleep()
      await asyncio.sleep(3)#3 секунды и убираем сообщение
      await msg.delete()        
      сhannel = client.get_channel(703653241027821658)
      emb = discord.Embed(title = 'Нарушение:', colour = discord.Color.red())#дальше сами логи тут уже ваша фантазия
      emb.add_field(name = 'Имя:', value = f'{message.author.name}', inline=False) #
      emb.add_field(name = 'Причина:', value = f'Мат({mes})')
      emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
      emb.set_footer(text = 'Спасибо за использования нашего бота')

      await ctx.send(embed = emb) #вывод embed 

# Очистка чата
@client.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(703653241027821658) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

# Работа с ошибками очистки чата

@clear.error
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c))     





@client.command()
async def feedback(ctx, *, arg = None):
    if arg is None:
        await ctx.send(embed=discord.Embed(title="Нет аргумента!", description=f":x: **{ctx.author.mention}**, укажи **сообщение**, которое будет **отоброжатся** в отзыве. :x:", color=0xFF0000))
    else:
        emb = discord.Embed(title = 'Ваш отзыв был успешно отправлен!', description = f'**Ваш отзыв выглядит так:** {arg}', color=0x6fdb9e)
        emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
        
        messagechannel = 727898926895595571
        channel = ctx.bot.get_channel(messagechannel)
        
        embed = discord.Embed(title = 'Новый отзыв!', description = f'**Отзыв выглядит так:** {arg}', color=0x6fdb9e)
        embed.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)

@client.command()
async def Dobavit(ctx, *, arg = None):
    if arg is None:
        await ctx.send(embed=discord.Embed(title="Нет аргумента!", description=f":x: **{ctx.author.mention}**, укажи **сообщение**, которое будет **отоброжатся** в Улучшение. :x:", color=0xFF0000))
    else:
        emb = discord.Embed(title = 'Ваша команда или улучшение бота успешно отправлено!', description = f'**Ваш улучшение или комапнда выглядит так:** {arg}', color=0x6fdb9e)
        emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
        
        messagechannel = 727898926895595571
        channel = ctx.bot.get_channel(messagechannel)
        
        embed = discord.Embed(title = 'Новый улучшение или команда для бота!', description = f'**Улучшение выглядит так:** {arg}', color=0x6fdb9e)
        embed.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)

@client.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 696445498126762049) #Айди роли
        channel_log = client.get_channel(703653241027821658) #Айди канала логов

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))  



    
# Работа с ошибками мута

@mute.error 
async def mute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))    

# Размут

@client.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 696445498126762049) #Айди роли
        channel_log = client.get_channel(703653241027821658) #Айди канала логов

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c))    

# Работа с ошибками размута

@unmute.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

# Кик
@client.command()
async def popygai( ctx, arg):
    embed = discord.Embed(title = arg, color = 0xe4b400)
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(703653241027821658) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками кика

@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

# Бан    

@client.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(703653241027821658) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

from discord.ext import commands, tasks
import discord
from discord.utils import get as getD
import mpu
import asyncio as ass
import pydoc

@client.command(name = "code")
async def evals(tx,*,code:str):
    role1 = 696445498139082754
    role2 = 756109141327740959
    role3 = 756953215341297695
    role4 = 757153272128733242
    usL = [getD(tx.message.guild.roles, id=role1),getD(tx.message.guild.roles, id=role2),getD(tx.message.guild.roles, id=role3),getD(tx.message.guild.roles, id=role4)]
    python = '```py\n{}\n```'
    if usL[0] in tx.author.roles or usL[1] in tx.author.roles or usL[2] in tx.author.roles or tx.author.permissions_in(tx.message.channel).kick_members == True: #слишком длино
        python = '```py\n{}\n```'
        code = code.replace("   "," ")
        code = """
async def yep(ctx,client,code,usL):
    """ + code + "\n" + """
try:
    client.loop.create_task(yep(tx,client,code,usL))
except Exception as e:
    async def yeps(tx,python,code):
        await tx.send(python.format(type(e).__name__ + ': ' + str(e)))
        await tx.send(python.format(code))
    client.loop.create_task(yeps(tx,python,code))
"""
        try:
            exec(code)
        except Exception as e:
            await tx.send(python.format(type(e).__name__ + ': ' + str(e)))
            await tx.send(python.format(code))
            return
    else:
        await tx.send(python.format("clownException: you clown (:")) #вот бы работало как надо


# Работа с ошибками бана

@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

@client.event
async def on_message(msg):
    print(msg.content)
    if msg.content == f'<@!{client.user.id}>' or  msg.content == f'<@{client.user.id}>':
        await msg.channel.send('Префикс бота D. что-бы узнать мои команды напиши D.help')
        return
    await client.process_commands(msg) 



token = open('token.txt', 'r').readline()
client.run( token )
#i
#i
#i
#i
#i
#i
#i