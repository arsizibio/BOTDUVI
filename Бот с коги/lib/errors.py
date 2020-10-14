from discord.ext import commands
class TimeoutException(Exception):
    pass
class AlreadyLoaded(Exception):
    pass
class MaximumBalanceError(Exception):
    pass
class LevelingIsDisabled(Exception):
    pass
class CreditIsDisabled(commands.CheckFailure):
    pass
class CommandIsDisabled(Exception):
    pass
class CommandOnCooldown(commands.CheckFailure):
    def __init__(self, message, *args, retry_after: int = 0):
        super().__init__(message, *args)
        self.retry_after = retry_after