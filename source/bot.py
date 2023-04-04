from os import environ # для получения переменных окружения
import discord
from discord.ext import commands # поддержка красивых команд
import gitlab # прикол




gl = gitlab.Gitlab(url = 'https://gitlab.megu.one',
	private_token = environ.get("TOKEN_GITLAB"))

project = gl.projects.get(13)



intents = discord.Intents.default()
intents.message_content = True

discord_bot = discord.Client(intents=intents)



    
@discord_bot.event
async def on_message(message):
	if message.author == discord_bot.user:
		return

	issue_text = message.content.replace("/issue ","") # Получение текста команды «issue»

	if message.content.startswith('/issue'): # Создание на базе этого задачи на ГитЛабе и отчёт об этом в канал
		if project.issues.create({'title': issue_text,'description': 'Something useful here.'}):
			await message.channel.send("Задача «" + issue_text + "» создана.")

discord_bot.run(environ.get("TOKEN_DISCORD"))