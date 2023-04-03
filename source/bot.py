import discord
import gitlab

gl = gitlab.Gitlab(url='https://gitlab.megu.one', private_token='glpat-FsbtfebnSiw1SJ8foYpu')

project = gl.projects.get(13)

print(type(gl.issues.list()))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/issue'):
        project.issues.create({'title': message.content.replace("/issue",""),'description': 'Something useful here.'})


client.run("MTA5MjQ3ODUzMTIyNjgzNjk5NA.Gbro_i.C9kbltoL-dCEpNC8e23WHPWnUd5BPaSE4TmWGQ")