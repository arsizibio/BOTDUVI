import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import sqlite3
import asyncio
import json
import requests
from Cybernator import Paginator
import jishaku
import wikipedia

class logs(commands.Cog):
    """LOGS Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print(' - Запущен')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        if not member.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        if after.channel == None:
            if not before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(725416079723200584) # Сюда свой канал логов
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) вышел из голосового канала 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Выход из канала', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                return await channel.send(embed = e)

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if member.bot:
                return
            channel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
            e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) перешёл в другой голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = f'Журнал аудита | Переход в канал', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
            e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
            e.add_field(name = "ID Участника", value = f"**{member.id}**")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            return await channel.send(embed = e)

        if not after.channel == None:
            if before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) зашёл в голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Вход в канал', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'ayf', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        rguild = self.bot.get_guild(721559151775318046) # Сюда ид своей гильдии

        if not before in rguild.members:
            return

        if before.avatar_url == after.avatar_url:
            return

        channel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        e = discord.Embed(description = f'**Пользователь {before.display_name}({before.mention}) изменил свой аватар!**', colour = before.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Измнение пользователя', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        e.add_field(name = "Новая аватарка", value = f"**[Кликабельная ссылка]({before.avatar_url})**")
        e.add_field(name = "ID Участника", value = f"**{before.id}**")
        e.set_image(url = after.avatar_url)
        e.set_thumbnail(url = before.avatar_url)
        e.set_footer(text = f'p', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        if not channel.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        chanel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        async for entry in chanel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create):
            if entry.user.bot:
                return
            e = discord.Embed(colour = entry.user.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Создание канала', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Канал:", value = f"<#{entry.target.id}>")
            e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
            e.add_field(name = "Создал:", value = f"{entry.user.mention}")
            e.add_field(name = "ID создавшего:", value = f"{entry.user.id}")
            e.set_footer(text = f'da lya', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            await chanel.send(embed = e)
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not channel.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        chanel = self.bot.get_channel(577534134692610081) # Сюда ид канала логов
        async for entry in chanel.guild.audit_logs(action = discord.AuditLogAction.channel_delete):
            if entry.user.bot:
                return
            e = discord.Embed(colour = entry.user.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Удаление канала', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Канал:", value = f"{channel.name}")
            e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
            e.add_field(name = "Удалил:", value = f"{entry.user.mention}")
            e.add_field(name = "ID удалившего:", value = f"{entry.user.id}")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            return await chanel.send(embed = e)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        if not role.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        chanel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        async for entry in chanel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create):
            e = discord.Embed(colour = role.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Создание роли', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Роль:", value = f"<@&{entry.target.id}>")
            e.add_field(name = "ID роли:", value = f"{entry.target.id}")
            e.add_field(name = "Создал:", value = f"{entry.user.mention}")
            e.add_field(name = "ID создавшего:", value = f"{entry.user.id}")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            await chanel.send(embed = e)
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not role.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        chanel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        async for entry in chanel.guild.audit_logs(action = discord.AuditLogAction.role_delete):
            e = discord.Embed(colour = role.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Удаление роли', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Роль:", value = f"{role.name}")
            e.add_field(name = "ID роли:", value = f"{entry.target.id}")
            e.add_field(name = "Удалил:", value = f"{entry.user.mention}")
            e.add_field(name = "ID удалившего:", value = f"{entry.user.id}")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            return await chanel.send(embed = e)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        if message.author.bot:
            return

        channel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        e = discord.Embed(colour = message.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Удаление сообщения', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        e.add_field(name = "Удалённое сообщение", value = f"```{message.content}```")
        e.add_field(name = "Автор", value = f"**{message.author.display_name}({message.author.mention})**")
        e.add_field(name = "Канал", value = f"**{message.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{message.id}**")
        e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return
        
        if before.content == after.content:
            return

        if before.author.bot:
            return

        channel = self.bot.get_channel(725416079723200584) # Сюда ид канала логов
        e = discord.Embed(description = f'**[Сообщение]({before.jump_url}) было изменено.**', colour = before.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Изменение сообщения', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        e.add_field(name = "Старое содержимое", value = f"```{before.content}```")
        e.add_field(name = "Новое соодержиое", value = f"```{after.content}```")
        e.add_field(name = "Автор", value = f"**{before.author.display_name}({before.author.mention})**")
        e.add_field(name = "Канал", value = f"**{before.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{before.id}**")
        e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.guild.id == 721559151775318046: # Сюда ид своей гильдии
            return

        if not len(before.roles) == len(after.roles):
            role = [ ]
            if len(before.roles) > len(after.roles):
                for i in before.roles:
                    if not i in after.roles:
                        role.append(f'➖ Была убрана роль {i.name}(<@&{i.id}>)\n')
            elif len(before.roles) < len(after.roles):
                for i in after.roles:
                    if not i in before.roles:
                        role.append(f'➕ Была добавлена роль {i.name}(<@&{i.id}>)\n')
            
            str_a = ''.join(role)
            channel = self.bot.get_channel(735782444569067530) # Сюда ид канала логов
            e = discord.Embed(description = f'**У пользователя {after.display_name}({after.mention}) были изменены роли.**', colour = before.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = f'Журнал аудита | Изменение ролей участника', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Было сделано", value = f"**{str_a}**")
            e.add_field(name = "ID Участника", value = f"**{after.id}**")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            return await channel.send(embed = e)

        if not before.display_name == after.display_name:
            channel = self.bot.get_channel(735782444569067530) # Сюда ид канала логов
            e = discord.Embed(description = f'**Пользователь {before.display_name}({after.mention}) изменил NickName**', colour = before.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = f'Журнал аудита | Изменение NickName участника', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            e.add_field(name = "Действующее имя", value = f"**{after.display_name}({after.mention})**")
            e.add_field(name = "Предыдущее имя", value = f"**{before.display_name}({before.mention})**")
            e.add_field(name = "ID Участника", value = f"**{after.id}**")
            e.set_footer(text = f'AYF', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            await channel.send(embed = e)


def setup(bot):
    bot.add_cog(logs(bot))