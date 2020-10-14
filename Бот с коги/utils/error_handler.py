from discord.ext import commands
import discord, traceback, humanize
from lib.botclass import Bot
import lib.errors as silentic_errors
from lib.api import post_text
import datetime

class ErrorHandler(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        error = getattr(error, 'original', error)
        if not isinstance(error, silentic_errors.CommandOnCooldown):
            try: ctx.reset_cooldown()
            except: pass
        
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.guild_only")}')
        if isinstance(error, silentic_errors.CreditIsDisabled):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.credits_is_disabled")}')
        if isinstance(error, silentic_errors.LevelingIsDisabled):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.leveling_is_disabled")}')
        if isinstance(error, silentic_errors.CommandIsDisabled):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.command_is_disabled_on_this_server")}')
        if isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.dm_only")}')
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.disabled_command")}')
        if isinstance(error, commands.NotOwner):
            return await ctx.message.add_reaction(self.bot.icon("forbidden"))
        if isinstance(error, silentic_errors.MaximumBalanceError):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.max_balance", max_balance=self.bot.config["max_balance"])}')
        if isinstance(error, silentic_errors.TimeoutException):
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.timeout")}')
        if isinstance(error, silentic_errors.CommandOnCooldown):
            retry_after = str(datetime.timedelta(seconds=int(error.retry_after)))
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.on_cooldown", time=retry_after.split(".")[0])}')
        if isinstance(error, commands.MissingPermissions):
            perms = '; '.join([str(x) for x in error.missing_perms])
            return await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("errors.missing_permissions", command=str(ctx.command), missing_perms=perms)}')
        if isinstance(error, commands.BadArgument):
            return await ctx.invoke(self.bot.get_command("help"), command=str(ctx.command))
        if isinstance(error, commands.UserInputError):
            return await ctx.invoke(self.bot.get_command("help"), command=str(ctx.command))
            
        try:
            await ctx.send(f'{self.bot.icon("error")} | {ctx.l10n("erorrs.happend_error")}', embed=discord.Embed(description=ctx.l10n("erorrs.happend_error.description")))
        except: pass
        err = "\n".join(traceback.format_exception(type(error), error, error.__traceback__))
        chn = await self.bot.fetch_channel(self.bot.config['channels']['logs']['errors'])
        try:
            await chn.send(embed=discord.Embed(description=f'Вызвана {ctx.author} в {ctx.guild} > {ctx.channel}'[:1000]) \
                .add_field(name='Сообщение', value=ctx.message.content, inline=False) \
                .add_field(name='Ошибка', value=f'```py\n{err}\n```', inline=False) \
                .set_author(name=f'Ошибка при выполнении команды {ctx.command}', icon_url=self.bot.icon("warning").url))    
        except:
            content = await post_text(ctx.message.content)
            error = await post_text(err)
            await chn.send(embed=discord.Embed(description=f'Вызвана {ctx.author} в {ctx.guild} > {ctx.channel}'[:1000]) \
                .add_field(name='Сообщение', value=content, inline=False) \
                .add_field(name='Ошибка', value=error, inline=False) \
                .set_author(name=f'Ошибка при выполнении команды {ctx.command}', icon_url=self.bot.icon("warning").url))


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))