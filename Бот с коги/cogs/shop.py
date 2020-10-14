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

    @commands.group(name='shop', invoke_without_command=True)
    async def shop(self, ctx):
        '''eco.shop.desc'''
        embed = discord.Embed(title=ctx.l10n('eco.shop.desc'))
        embed.add_field(name='`boost`: ' + ctx.l10n('eco.shop.boost.title'), value=ctx.l10n('eco.shop.boost.desc') + ' | ' + ctx.l10n('eco.shop.boost.cost'), inline=False)
        shop = self.bot.load_json('data/shop.json')
        if str(ctx.guild.id) not in shop: shop[str(ctx.guild.id)] = {}
        guildShop = []
        for roleId in shop[str(ctx.guild.id)]:
            role = shop[str(ctx.guild.id)][roleId]
            if roleId not in [str(x.id) for x in ctx.guild.roles]:
                continue
            roleName = [str(x.name) for x in ctx.guild.roles if str(x.id) == roleId][0]
            guildShop.append(f'`{roleName}` - {ctx.l10n("eco.shop.guild.role", roleID=roleId)} | {ctx.l10n("eco.shop.cost", cost=role["cost"])}')
        if guildShop != []:
            embed.add_field(name=ctx.l10n("eco.shop.guild"), value='\n'.join(guildShop))
        embed.set_footer(text=ctx.l10n('eco.shop.howTo'))
        await ctx.send(embed=embed)
    @shop.command(name='buy')
    async def buy(self, ctx, *, item):
        '''eco.shop.buy.desc'''
        shop = self.bot.load_json('data/shop.json')
        try:
            if str(ctx.guild.id) not in shop: shop[str(ctx.guild.id)] = {}
            items = {discord.utils.get(ctx.guild.roles, id=int(y)).name: y for y in shop[str(ctx.guild.id)]}
        except: items = []
        if item == 'boost':
            if self.get_coins(ctx.author) < 1000:
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.buy.not_enough")}')
            if self.get_boost(ctx.author) >= 10:
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.buy.error.boost")}')
            self.set_coins(ctx.author, self.get_coins(ctx.author)-1000)
            self.set_boost(ctx.author, self.get_boost(ctx.author)+1)
            await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.shop.buy.ok", item=item)}')
        else:
            found = [x for x in items if x.find(item) != -1]
            if found != []:
                roleId = items[found[0]]
                role = discord.utils.get(ctx.guild.roles, id=int(roleId))
                confirm = await ctx.confirm(discord.Embed(title=ctx.l10n('eco.shop.buy.confirm', item=role.name.replace("@","@\u200b"))))
                if not confirm: return
                if shop[str(ctx.guild.id)][str(roleId)]['cost'] > self.get_coins(ctx.author):
                    return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.buy.not_enough")}')
                await ctx.author.add_roles(role)
                self.set_coins(ctx.author, self.get_coins(ctx.author)-shop[str(ctx.guild.id)][str(roleId)]['cost'])
                await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.shop.buy.ok", item=item)}')
            else:
                items = [f'``boost`` - {ctx.l10n("eco.shop.boost.desc")} | {ctx.l10n("eco.shop.boost.cost")}']
                if str(ctx.guild.id) not in shop: shop[str(ctx.guild.id)] = {}
                for roleId in shop[str(ctx.guild.id)]:
                    role = shop[str(ctx.guild.id)][roleId]
                    if roleId not in [str(x.id) for x in ctx.guild.roles]:
                        continue
                    roleName = discord.utils.get(ctx.guild.roles, id=int(roleId)).name
                    items.append(f'`{roleName}` - {ctx.l10n("eco.shop.guild.role", roleID=roleId)} | {ctx.l10n("eco.shop.cost", cost=role["cost"])}')
                embed = discord.Embed(description='\n'.join(items))
                return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.buy.unknown", item=item)}', embed=embed)

    @shop.command(name='add-role')
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, cost: int):
        '''eco.shop.addrole.desc'''
        if role.permissions > ctx.author.guild_permissions or role.position >= ctx.author.top_role.position:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.addrole.missing_permissions")}')
        if cost < 10:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.addrole.minimum_cost")}')
        if cost > self.bot.config['max_balance']:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.addrole.maximum_cost", value=self.bot.config["max_balance"])}')
        shop = self.bot.load_json('data/shop.json')
        if str(ctx.guild.id) not in shop: shop[str(ctx.guild.id)] = {}
        if str(role.id) in shop[str(ctx.guild.id)]:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.addrole.exists")}')
        shop[str(ctx.guild.id)][str(role.id)] = {'cost': cost}
        self.bot.write_json('data/shop.json', shop)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.shop.addrole.ok")}')
    @shop.command(name='remove-role')
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, role: discord.Role):
        '''eco.shop.addrole.desc'''
        if role.permissions > ctx.author.guild_permissions or role.position >= ctx.author.top_role.position:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.removerole.missing_permissions")}')
        shop = self.bot.load_json('data/shop.json')
        if str(ctx.guild.id) not in shop: shop[str(ctx.guild.id)] = {}
        if str(role.id) not in shop[str(ctx.guild.id)]:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.shop.removerole.unknown")}')
        del shop[str(ctx.guild.id)][str(role.id)]
        self.bot.write_json('data/shop.json', shop)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.shop.removerole.ok")}')
def setup(bot: Bot):
    bot.add_cog(Economy(bot))