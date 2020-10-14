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

    async def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Guild only')
        return True

    def get_cooldown(self, ctx):
        try:
            rules = self.bot.load_json('data/rules.json')
            return rules['cooldown'][str(ctx.command.name)][str(ctx.guild.id)]
        except:
            return None
    def credit_time_passed(self, timestamp: float):
        return (datetime.now() - datetime.utcfromtimestamp(timestamp)).total_seconds() / 60 
    def get_credit_amount(self, user):
        credit = self.bot.load_json('data/credit_claimed.json')
        if str(user.guild.id) not in credit: return 0
        if str(user.id) not in credit[str(user.guild.id)]: return 0
        return self.get_bank(user) + round(self.credit_time_passed(credit[str(user.guild.id)][str(user.id)]))
    def get_reputation(self, user):
        reputation = self.bot.load_json('data/reputation.json')
        if str(user.guild.id) not in reputation: return 0.0
        if str(user.id) not in reputation[str(user.guild.id)]: return 0.0
        return reputation[str(user.guild.id)][str(user.id)]
    def set_reputation(self, user, amount: float):
        reputation = self.bot.load_json('data/reputation.json')
        if str(user.guild.id) not in reputation: reputation[str(user.guild.id)] = {}
        reputation[str(user.guild.id)][str(user.id)] = abs(amount)
        self.bot.write_json('data/reputation.json', reputation)
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

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        '''eco.balance.desc'''
        if not user: user = ctx.author
        img = Image.open('assets/img/balance.png')
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("assets/font/Comfortaa.ttf", 40)
        if self.get_coins(user) > 99999:
            coinFont = ImageFont.truetype("assets/font/Comfortaa.ttf", 30)
        else:
            coinFont = ImageFont.truetype("assets/font/Comfortaa.ttf", 35)
        if self.get_credit_amount(user) > 99999:
            creditFont = ImageFont.truetype("assets/font/Comfortaa.ttf", 30)
        else:
            creditFont = ImageFont.truetype("assets/font/Comfortaa.ttf", 35)
        d.text((145, 47), ctx.l10n("eco.balance.coins", coins=str(self.get_coins(user))[:8]), font=coinFont, fill=(255,255,255,255))
        d.text((145, 100), ctx.l10n('eco.balance.bank', bank=str(self.get_credit_amount(ctx.author))[:8]), font=creditFont, fill=(255,255,255,255))
        d.text((490, 40), str(self.get_boost(user)), font=font, fill=(255,255,255,255))
        d.text((490, 110), str(self.get_reputation(user)), font=font, fill=(255,255,255,255))
        avatar_size = (100, 100)
        mask = Image.new('L', avatar_size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + avatar_size, fill=255)
        response = requests.get(str(user.avatar_url_as(format='png')))
        avatar = Image.open(BytesIO(response.content))  
        avatar = avatar.resize(avatar_size, Image.ANTIALIAS)
        avatar = ImageOps.fit(avatar, mask.size, centering=(0.4, 0.4))
        avatar.putalpha(mask)
        img.paste(avatar, (30,43), avatar)
        byte = BytesIO()
        img.save(byte, 'PNG')
        byte.seek(0)
        await ctx.send(file=discord.File(byte, filename=f'balance.png'))    
    
    @commands.command(name='respect')
    @checks.cooldown(3600*24)
    async def respect(self, ctx, member: discord.Member):
        '''eco.respect.desc'''
        ctx.set_cooldown(self.get_cooldown(ctx))
        if member.id == ctx.author.id:
            ctx.reset_cooldown()
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.respect.fail.0")} ')
        if member.bot:
            ctx.reset_cooldown()
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.respect.fail.1")} ')
        self.set_reputation(member, self.get_reputation(member)+0.1)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.respect.ok", user=str(member))} ')
    @commands.command(name='pay')
    @checks.cooldown(10)
    async def pay(self, ctx, to: discord.Member, amount: int):
        '''eco.pay.desc'''
        ctx.set_cooldown(self.get_cooldown(ctx))
        confirm = await ctx.confirm(discord.Embed(title=ctx.l10n('eco.pay.confirm', user=str(to), amount=amount)))
        if not confirm: return
        if amount < 10: return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.pay.fail.0")} ')
        if to.bot: return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.pay.fail.1")} ')
        if to.id == ctx.author.id: return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.pay.fail.2")} ')
        if amount > self.get_coins(ctx.author): return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.pay.fail.3")} ')
        self.set_coins(ctx.author, self.get_coins(ctx.author)-amount)
        self.set_coins(to, self.get_coins(to)+amount)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.pay.ok")}')
    @commands.command(name='lottery')
    @checks.cooldown(30)
    async def lottery(self, ctx, amount: int):
        '''eco.lottery.desc'''
        ctx.set_cooldown(self.get_cooldown(ctx))
        if amount > self.get_coins(ctx.author):
            ctx.reset_cooldown()
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.lottery.fail.0")} ')
        if amount < 45:
            ctx.reset_cooldown()
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.lottery.fail.1")} ')
        won = bool(random.randint(0,1))
        if won:
            coins = random.randint(int(amount/3), int(amount*3))
            self.set_coins(ctx.author, self.get_coins(ctx.author)+coins)
            await ctx.send(embed=discord.Embed(title=ctx.l10n('eco.lottery') + ' | ' + ctx.l10n('eco.lottery.won', coins=coins)))
        else:
            coins = random.randint(int(amount/3), amount)
            self.set_coins(ctx.author, self.get_coins(ctx.author)-coins)
            await ctx.send(embed=discord.Embed(title=ctx.l10n('eco.lottery') + ' | ' + ctx.l10n('eco.lottery.lose', coins=coins)))

    @commands.command(name='work')
    @checks.cooldown(3600*2)
    async def work(self, ctx):
        '''eco.work.desc'''
        ctx.set_cooldown(self.get_cooldown(ctx))
        item = random.choice(ctx.l10n("eco.work.texts.items"))
        place1 = random.choice(ctx.l10n("eco.work.texts.places1"))
        place2 = random.choice(ctx.l10n("eco.work.texts.places2", place1=place1))
        coins = random.randint(100, 500)
        text = random.choice(ctx.l10n('eco.work.texts.all', place1=place1, place2=place2, item=item, coins=coins))
        embed = discord.Embed(title=text)
        boost = self.get_boost(ctx.author)
        if boost > 0:
            coins = coins + boost * 50
            embed.add_field(name=f'{self.bot.icon("boost")} | {ctx.l10n("eco.work.boost", boost=boost)}', value=ctx.l10n('eco.work.boost.got', amount=boost * 50))
        self.set_coins(ctx.author, self.get_coins(ctx.author)+coins)
        await ctx.send(embed=embed)
    
    @commands.group(name='credit', invoke_without_command=True)
    @checks.credit_enabled()
    async def credit(self, ctx):
        '''eco.credit.desc'''
        await ctx.call_help()
    @credit.command(name='pay')
    @checks.credit_enabled()
    async def cpay(self, ctx):
        '''eco.credit.pay.desc'''
        if self.get_bank(ctx.author) == 0:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.status.not_claimed")}')
        to_pay = self.get_credit_amount(ctx.author)
        if self.get_coins(ctx.author) < to_pay:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.pay.fail", amount=to_pay)}')
        self.set_coins(ctx.author, self.get_coins(ctx.author)-to_pay)
        self.set_bank(ctx.author, 0)
        try:
            credit = self.bot.load_json('data/credit_claimed.json')
            del credit[str(ctx.guild.id)][str(ctx.author.id)]
            self.bot.write_json('data/credit_claimed.json', credit)
        except: pass    
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.credit.pay.ok")}')
    @credit.command(name='claim')
    @checks.credit_enabled()
    async def cclaim(self, ctx, amount: int):
        '''eco.credit.claim.desc'''
        if self.get_bank(ctx.author) > 0:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.claim.fail.already")}')
        if amount > 1000:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.claim.fail.tooBig")}')
        if amount < 10:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.claim.fail.tooSmall")}')
        self.set_coins(ctx.author, self.get_coins(ctx.author)+amount)
        self.set_bank(ctx.author, amount)
        credit = self.bot.load_json('data/credit_claimed.json')
        if str(ctx.guild.id) not in credit: credit[str(ctx.guild.id)] = {}
        credit[str(ctx.guild.id)][str(ctx.author.id)] = time.time()
        self.bot.write_json('data/credit_claimed.json', credit)
        await ctx.send(f'{self.bot.icon("done")} | {ctx.l10n("eco.credit.claim.ok")}', embed=discord.Embed().set_footer(text=ctx.l10n('eco.credit.claim.ok.footer')))
    @credit.command(name='status')
    @checks.credit_enabled()
    async def cstatus(self, ctx):
        '''eco.credit.status.desc'''
        if self.get_bank(ctx.author) == 0:
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.credit.status.not_claimed")}')
        embed = discord.Embed(title=ctx.l10n('eco.credit.status.desc'))
        embed.add_field(name=ctx.l10n('eco.credit.status.total'), value=self.get_bank(ctx.author))
        embed.add_field(name=ctx.l10n('eco.credit.status.pay'), value=self.get_credit_amount(ctx.author))
        credit = self.bot.load_json('data/credit_claimed.json')
        embed.add_field(name=ctx.l10n('eco.credit.status.time_passed'), value=round(self.credit_time_passed(credit[str(ctx.guild.id)][str(ctx.author.id)])/60, 2))
        await ctx.send(embed=embed)
    @commands.command(name='top', aliases=['leaderboard'])
    async def leaderboard(self, ctx):
        '''eco.top'''
        coins = self.bot.load_json('data/coins.json')['coins']
        if str(ctx.guild.id) not in coins: return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("eco.top.fail")}')
        coins = coins[str(ctx.guild.id)]
        embed = discord.Embed(title=ctx.l10n('eco.top'))
        ld = []
        csorted = sorted(coins, key=lambda i: coins[i], reverse=True)
        me = None
        for user in csorted:
            if str(user) == str(ctx.author.id): me = len(ld)+1
            try:
                username = discord.utils.get(ctx.guild.members, id=int(user)).display_name
            except:
                username = 'invalid-user'
            ld.append(ctx.l10n('eco.top.bal', place=len(ld)+1, user=username, balance=coins[str(user)]))
        desc = []
        if me:
            desc.append(ctx.l10n('eco.top.you', place=me, bal=coins[str(ctx.author.id)]))
        desc.append('')
        desc += ld
        embed.description = '\n'.join(desc)
        await ctx.send(embed=embed)
def setup(bot: Bot):
    bot.add_cog(Economy(bot))