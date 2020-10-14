from aiohttp import ClientSession
import urllib.parse, json
async def dsapi_sendMessage(token, channel, messageContent):
    async with ClientSession() as session:
        async with session.post(f'https://discordapp.com/api/channels/{channel}/messages',
                                data={'content': messageContent},
                                headers={'Authorization': f'Bot {token}'}) as data:
            return await data.json()
    
async def post_text(content):
    async with ClientSession() as session:
        async with session.post(f'https://silentic.xyz/cdn/post.php', data={'content': content}) as data:
            return f'https://silentic.xyz/cdn/{(await data.text())}'
async def check_token(token):
    async with ClientSession() as session:
        async with session.get(f'https://discordapp.com/api/users/@me', headers={'Authorization': f'Bot {token}'}) as data:
            return await data.json()
async def create_gist(description, files: dict, public: bool = True):
    async with ClientSession() as session:
        async with session.post('https://api.github.com/gists',
            headers={'Authorization':'token fb517b733897535006769e9777fec9f01e5b99bd', 'Content-Type': 'application/json'},
            data=json.dumps({"public":public,"description":description,"files":files})) as resp:
            return (await resp.json())['id']
async def delete_gist(gist_id):
    async with ClientSession() as session:
        async with session.delete(f'https://api.github.com/gists/{gist_id}',
            headers={'Authorization':'token fb517b733897535006769e9777fec9f01e5b99bd', 'Content-Type': 'application/json'}) as resp:
            return (await resp.text())