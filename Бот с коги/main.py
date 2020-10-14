from discord.ext import commands
import discord, datetime, os, colorama, traceback
from colorama import Style, Fore
import lib.errors as s_errors
import yaml, io, sys, asyncio
import json
colorama.init()

PREFIX = '!'

class Silentic:
    def __init__(self):
        bot = commands.bot(command_prefix=PREFIX)
        self.config = None
        self.started_at = datetime.datetime.now()
        self.remove_command('help')
        self.load_config()
        self.load()
        self.load_locales()
        self.exc_debug = {
            'commands': [],
            'writes': [],
            'reads': [],
            'updated_at': 0
        }
        self.workspace = lib.workspace.workspace()

    def load_json(self, file):
        self.exc_debug['reads'].append(len(self.exc_debug['reads'])+1)
        return json.loads(io.open(file, mode='r', encoding='utf-8').read())
    def write_json(self, file, data: dict):
        self.exc_debug['writes'].append(len(self.exc_debug['writes'])+1)
        io.open(file, mode='w', encoding='utf-8').write(json.dumps(data))

    def load_config(self):
        print('Loading config...')
        self.config = yaml.safe_load(io.open('config.yaml', mode='r', encoding='utf-8'))
        print('Config loaded')

    async def get_prefix(self, msg):
        prefix = commands.when_mentioned_or(*self.config['prefixes'])
        try:
            prefixes = self.load_json('data/prefixes.json')
            if msg.guild and str(msg.guild.id) in prefixes['guild']:
                prefix = commands.when_mentioned_or(prefixes['guild'][str(msg.guild.id)])
            if str(msg.author.id) in prefixes['self']:
                prefix = commands.when_mentioned_or(prefixes['self'][str(msg.author.id)])
        except:
            pass
        return prefix(self, msg)

    def load_locales(self):
        self.locales = {x.name.split('.')[0]:{} for x in os.scandir('locale') if x.name.endswith('.yaml')}
        print(f'Loading {len(self.locales)} locales... ({list(self.locales)}){Style.RESET_ALL}')
        for locale in self.locales:
            print(f'{Fore.LIGHTBLACK_EX}Loading locale {locale}...{Style.RESET_ALL}')
            try:
                self.locales[locale] = yaml.safe_load(io.open(f'locale/{locale}.yaml', mode='r', encoding='utf-8'))
            except:
                print(f'{Fore.LIGHTRED_EX}Error when loading locale {locale}:\n{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}')
            else:
                print(f'{Fore.GREEN}Locale {locale} loaded{Style.RESET_ALL}')

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=SilenticContext)

    async def status_change_loop(self):
        while True:
            statuses = (
                f'{len(self.guilds)} guilds | s.help',
                f'{len(self.users)} users | s.help',
                f'{len(self.emojis)} emojis | s.help'
            )
            types = {'listening': discord.ActivityType.listening, 'watching': discord.ActivityType.watching}
            aType = discord.ActivityType.playing
            if 'type' in self.config['startActivity'] and self.config['startActivity']['type'] in types:
                aType = types[self.config['startActivity']['type']]
            for status in statuses:
                await self.change_presence(activity=discord.Activity(type=aType, name=status))
                await asyncio.sleep(15)

    async def exc_update(self):
        chn = await self.fetch_channel(self.config['channels']['logs']['status'])
        while True:
            try: exc_cmd = sum(self.exc_debug['commands']) / len(self.exc_debug['commands'])
            except ZeroDivisionError: exc_cmd = 0

            try: exc_writes = sum(self.exc_debug['writes']) / len(self.exc_debug['writes'])
            except ZeroDivisionError: exc_writes = 0

            try: exc_reads = sum(self.exc_debug['reads']) / len(self.exc_debug['reads'])
            except ZeroDivisionError: exc_reads = 0

            await chn.send(f'``[{datetime.datetime.now()} UTC]`` Latency: {self.latency*100}ms | Average commands/minute: {exc_cmd} | Average writes/minute: {exc_writes} | Average reads/minute: {exc_reads}')
            self.exc_debug = {
                'commands': [],
                'writes': [],
                'reads': [],
                'updated_at': 0
            }
            await asyncio.sleep(900)

    async def on_ready(self):
        self.loaded_at = datetime.datetime.now()
        print(f'Bot ready | Logged in as {self.user.name}')
        if 'startActivity' in self.config:
            types = {'listening': discord.ActivityType.listening, 'watching': discord.ActivityType.watching}
            aType = discord.ActivityType.playing
            if 'type' in self.config['startActivity'] and self.config['startActivity']['type'] in types:
                aType = types[self.config['startActivity']['type']]
            await self.change_presence(activity=discord.Activity(name=self.config['startActivity']['name'], type=aType))
        await self.wait_until_ready()
        self.loop.create_task(self.status_change_loop())
        self.loop.create_task(self.exc_update())
    async def on_connect(self):
        self.connected_at = datetime.datetime.now()
        print('Websocket connected')

    def load(self):
        print('Loading modules...')
        self.moduleLoad_start = datetime.datetime.now()
        modules = ['jishaku']
        modules += [f'cogs.{x.name.split(".")[0]}' for x in os.scandir('cogs/') if x.name.endswith('.py')]
        modules += [f'utils.{x.name.split(".")[0]}' for x in os.scandir('utils/') if x.name.endswith('.py')]
        for module in modules:
            print(f'{Fore.LIGHTBLACK_EX}Loading module {module}...{Style.RESET_ALL}')
            try:
                self.load_extension(module)
            except:
                print(f'{Fore.LIGHTRED_EX}Error when loading module {module}:{Style.RESET_ALL}')
                print(f'{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}')
            else:
                print(f'{Fore.GREEN}Module {module} loaded{Style.RESET_ALL}')
        self.moduleLoad_end = datetime.datetime.now()
        print(f'All modules loaded in {(self.moduleLoad_end-self.moduleLoad_start).total_seconds()} seconds')

    async def restart_(self):
        self.logout()
        os.execl(sys.executable, sys.executable, *sys.argv)


    def restart(self):
        self.loop.create_task(self.restart_())

    async def is_owner(self, member):
        owners = [x.id for x in (await self.application_info()).team.members]
        return member.id in owners

token = open('token.txt', 'r').readline()
bot.run(token)


