'''	Интеграция Дискорда и ГитЛаба
🄯	Стешенко Артём и Зажигин Богдан '''

'''	Справочные материалы на английском для разработки
Язык Пайтон —	https://docs.python.org/3.12/reference
АПИ Дискорда —	https://discordpy.readthedocs.io/en/latest
АПИ ГитЛаба —	https://python-gitlab.readthedocs.io/en/latest
'''


from os import environ, remove # получение переменных среды и удаление файлов
import discord, gitlab # работа с АПИ Дискорда и ГитЛаба
import csv # запись и чтение табличной базы данных, https://ru.wikipedia.org/wiki/CSV

database = open("database.csv", "w")
database.close()

slovar = dict()


gitlab_instance = gitlab.Gitlab(
	url = 'https://gitlab.megu.one', 
	private_token = environ.get("TOKEN_GITLAB")
)

project = gitlab_instance.projects.get(13) # TODO: надо чтобы id проекта привязался к id канала



intents = discord.Intents.default()
intents.message_content = True

discord_bot = discord.Client(intents=intents) # Объявление о существовании бота
#tree_commands = discord.app_commands.CommandTree(discord_bot) # Объявление дерева команд бота


    
@discord_bot.event
async def on_message(message): # обработка каждого сообщения
	if message.author == discord_bot.user: # самооигнор
		return

	issue_text = message.content.replace("/issue ","") # Получение текста команды «issue»

	if message.content.startswith('/issue'): # Создание на базе этого задачи на ГитЛабе и отчёт об этом в канал
		if project.issues.create({'title': issue_text,'description': 'Something useful here.'}):
			await message.channel.send("Задача «" + issue_text + "» создана.")
	
	#if message.content.startswith('/project'):
		#slovar.update({message.channel.id: message.content.replace("/project ","")})
		#await message.channel.send(slovar)

	if message.content.startswith('/project'):
		database = open("database.csv", "a+")
		database.write(str({message.channel.id: message.content.replace("/project ","")}) + "\n")
		database.close()
	
	if message.content.startswith('/remove'):
		remove("database.csv")

#command_issue_extras = dict()
#@tree_commands.command(name="issue", description="создать задачу на GitLab", nsfw=False, auto_locale_strings=False)
#async def issue(interaction):
#	await interaction.response.send_message(f"Pong", ephemeral=True)

#add_command(*command_issue, guild=None, guilds=None, override=True)
#asyncio.run(sync(*command_issue, guild=None))


discord_bot.run(environ.get("TOKEN_DISCORD"))