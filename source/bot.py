import discord
import gitlab

gl = gitlab.Gitlab(url='https://gitlab.megu.one', private_token='glpat-FsbtfebnSiw1SJ8foYpu')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/issue'):
        await message.channel.send(3 + 6)


client.run("MTA5MjQ3ODUzMTIyNjgzNjk5NA.GKB56y.LpYtwlRcUX6R2ZWe_HAZp6bAEUEBYDfMbHmX3A")