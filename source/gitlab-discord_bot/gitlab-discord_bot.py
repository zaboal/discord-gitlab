'''	Интеграция Дискорда и ГитЛаба
©	Стешенко Артём и Зажигин Богдан	2023—2023 '''

from os import environ, remove
	# Получение переменных среды и удаление файлов —
	# https://docs.python.org/3.12/library/os.html
import msgpack
	# Бинарная сериализация, создание машинной базы данных —
	# https://github.com/msgpack/msgpack-python/blob/main/README.md
import gitlab, discord 
	# Обертка АПИ ГитЛаба — https://python-gitlab.readthedocs.io/en/latest и
	# АПИ Дискорда — https://discordpy.readthedocs.io/en/latest


database = open("database.msgpack", "a+") # создать базу данных если её нет

if database.read(): # декодирует базу данных если она есть
	database_spisok = msgpack.unpackb(database.read())


gitlab_instance = gitlab.Gitlab(url = 'https://gitlab.megu.one', private_token = environ.get("TOKEN_GITLAB")) # определение адреса и токена экземляра ГитЛаба
project = gitlab_instance.projects.get(13) # определение проекта в котором нужно создавать задачи
	# TODO: Привязка экзепмляра и проекта к Дискорд Каналу в БД, а не в коде


intents = discord.Intents.default() # использовать требования по умолчанию
intents.message_content = True # требовать содержимое сообщений
	# Определение событий требуемых для функционирования бота, например, «пользователь печатает» можно игнорировать, а отправленное сообщение нужно получить

discord_bot = discord.Client(intents=intents) # определение конфигурации бота


    
@discord_bot.event
async def on_message(message): # обработка каждого сообщения
	if message.author == discord_bot.user: # самооигнор
		return

	issue_text = message.content.replace("/issue ","") # получение текста команды «issue»
	if message.content.startswith('/issue'): # команда создания задачи на ГитЛабе
		if project.issues.create({'title': issue_text}):
			await message.channel.send("Задача «" + issue_text + "» создана.")

	if message.content.startswith('/project'):
		database_spisok[int(message.channel.id)] = int(message.content.replace("/project ",""))
	
	if message.content.startswith('/remove'): # команда удаления базы данных
		remove("database.msgpack")

	if message.content.startswith('/show'):
		await message.channel.send(database_spisok.get(int(message.channel.id)))


discord_bot.run(environ.get("TOKEN_DISCORD")) # авторизация бота по токену из среды и запуск 


# TODO: Регистрировать команды бота в Команды Приложения —
# https://discordpy.readthedocs.io/en/latest/interactions/api.html#application-commands:
#=======================================================================

'''tree_commands = discord.app_commands.CommandTree(discord_bot) # Объявление дерева команд бота
	if message.content.startswith('/project'):
		slovar.update({message.channel.id: message.content.replace("/project ","")})
		await message.channel.send(slovar)
slovar = dict()
command_issue_extras = dict()
@tree_commands.command(name="issue", description="создать задачу на GitLab", nsfw=False, auto_locale_strings=False)
async def issue(interaction):
	await interaction.response.send_message(f"Pong", ephemeral=True)
add_command(*command_issue, guild=None, guilds=None, override=True)
asyncio.run(sync(*command_issue, guild=None))'''

#=======================================================================

'''database_file = open("database.msgpack", "w")
database = msgpack.unpackb(database_file.read()) # \31123\123123\123132\213
# {1: a}, {2: b}
Ctrl+c = SINGal TERMinate

database[3] = "c"
# {1: a}, {2: b}, {3, c}

# /save
database_file.write(
    msgpack.packb(database, use_bin_type=True) # \31123\123123\123132\213 + \123123123123
)
database_file.close()'''