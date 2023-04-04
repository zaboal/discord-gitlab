from os import environ # для получения переменных окружения
import discord
from discord.ext import commands # поддержка красивых команд
import gitlab # прикол




gl = gitlab.Gitlab(url = 'https://gitlab.megu.one',
	private_token = environ.get("TOKEN_GITLAB"))

project = gl.projects.get(13)
# надо чтобы id проекта привязался к id канала


intents = discord.Intents.default()
intents.message_content = True

discord_bot = discord.Client(intents=intents) # Объявление о существовании бота
#tree_commands = discord.app_commands.CommandTree(discord_bot) # Объявление дерева команд бота


    
@discord_bot.event
async def on_message(message):
	if message.author == discord_bot.user:
		return

	issue_text = message.content.replace("/issue ","") # Получение текста команды «issue»

	if message.content.startswith('/issue'): # Создание на базе этого задачи на ГитЛабе и отчёт об этом в канал
		if project.issues.create({'title': issue_text,'description': 'Something useful here.'}):
			await message.channel.send("Задача «" + issue_text + "» создана.")
	

#command_issue_extras = dict()
#@tree_commands.command(name="issue", description="создать задачу на GitLab", nsfw=False, auto_locale_strings=False)
#async def issue(interaction):
#	await interaction.response.send_message(f"Pong", ephemeral=True)

#add_command(*command_issue, guild=None, guilds=None, override=True)
#asyncio.run(sync(*command_issue, guild=None))









discord_bot.run(environ.get("TOKEN_DISCORD"))