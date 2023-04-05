'''	Интеграция Дискорда и ГитЛаба
🄯	Стешенко Артём и Зажигин Богдан '''

from os import environ, remove
	''' Получение переменных среды и удаление файлов —
		https://docs.python.org/3.12/library/os.html '''
import msgpack
	''' Бинарная сериализация, создание машинной базы данных —
		https://github.com/msgpack/msgpack-python/blob/main/README.md '''
import gitlab, discord 
	''' Обертка АПИ ГитЛаба — https://python-gitlab.readthedocs.io/en/latest и
		АПИ Дискорда — https://discordpy.readthedocs.io/en/latest '''


database = open("database.csv", "w")
database.close()


gitlab_instance = gitlab.Gitlab(url = 'https://gitlab.megu.one', private_token = environ.get("TOKEN_GITLAB")) # определение адреса и токена экземляра ГитЛаба
project = gitlab_instance.projects.get(13) # определение проекта в котором нужно создавать задачи
	''' TODO: Привязка экзепмляра и проекта к Дискорд Каналу в БД, а не в коде '''


intents = discord.Intents.default() # использовать требования по умолчанию
intents.message_content = True # требовать содержимое сообщений
	''' Определение событий требуемых для функционирования бота, например,
		«пользователь печатает» можно игнорировать, а отправленное сообщение нужно получить '''

discord_bot = discord.Client(intents=intents) # определение конфигурации бота


    
@discord_bot.event
async def on_message(message): # обработка каждого сообщения
	if message.author == discord_bot.user: # самооигнор
		return

	issue_text = message.content.replace("/issue ","") # получение текста команды «issue»

	if message.content.startswith('/issue'): # создание на базе этого задачи на ГитЛабе и отчёт об этом в канал
		if project.issues.create({'title': issue_text,'description': 'Something useful here.'}):
			await message.channel.send("Задача «" + issue_text + "» создана.")

	if message.content.startswith('/project'):
		database = open("database.csv", "a+")
		database.write(str({message.channel.id: message.content.replace("/project ","")}) + "\n")
		database.close()
	
	if message.content.startswith('/remove'):
		remove("database.csv")


discord_bot.run(environ.get("TOKEN_DISCORD"))


'''	TODO: Регистрировать команды бота в Команды Приложения —
	https://discordpy.readthedocs.io/en/latest/interactions/api.html#application-commands:

tree_commands = discord.app_commands.CommandTree(discord_bot) # Объявление дерева команд бота
	if message.content.startswith('/project'):
		slovar.update({message.channel.id: message.content.replace("/project ","")})
		await message.channel.send(slovar)
slovar = dict()
command_issue_extras = dict()
@tree_commands.command(name="issue", description="создать задачу на GitLab", nsfw=False, auto_locale_strings=False)
 async def issue(interaction):
	await interaction.response.send_message(f"Pong", ephemeral=True)
add_command(*command_issue, guild=None, guilds=None, override=True)
asyncio.run(sync(*command_issue, guild=None))
'''