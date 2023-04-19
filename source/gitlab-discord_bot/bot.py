'''	Интеграция Дискорда и ГитЛаба
©	Стешенко Артём и Зажигин Богдан	2023—2023 '''

from os import environ
	# Получение переменных среды и удаление файлов —
	# https://docs.python.org/3.12/library/os.html
import gitlab, discord 
	# Обертка АПИ ГитЛаба — https://python-gitlab.readthedocs.io/en/latest и
	# АПИ Дискорда — https://discordpy.readthedocs.io/en/latest



database_spisok = dict()


gitlab_instance = gitlab.Gitlab(url = 'https://gitlab.megu.one', private_token = environ.get("TOKEN_GITLAB")) # определение адреса и токена экземляра ГитЛаба


intents = discord.Intents.default() # использовать требования по умолчанию
intents.message_content = True # требовать содержимое сообщений
	# Определение событий требуемых для функционирования бота, например, «пользователь печатает» можно игнорировать, а отправленное сообщение нужно получить

discord_bot = discord.Client(intents=intents) # определение конфигурации бота
    
@discord_bot.event
async def on_message(message): # обработка каждого сообщения
	command = message.content.startswith
	reply = message.channel.send

	if message.author == discord_bot.user: # самооигнор
		return

	issue_text = message.content.replace("/issue ","") # получение текста команды «issue»
	if command('/issue'): # команда создания задачи на ГитЛабе
		if database_spisok.get(int(message.channel.id)):
			project = gitlab_instance.projects.get(str(database_spisok.get(int(message.channel.id))))
			if project.issues.create({'title': issue_text}):
				await reply("Задача «" + issue_text + "» создана успешно, ^w^")
			else:
				await reply("не получилось, QwQ")
		else:
			await reply("данных нет, введите пожалуйста id для подключения через /project (id проекта), ^w^")

	if command('/project'):
		try:
			database_spisok[int(message.channel.id)] = int(message.content.replace("/project ",""))
			await reply("данные сохранены ^w^")
		except:
			await reply("не удалось сохранить id")
	
	if command('/remove'): # команда удаления базы данных
		try:
			remove("database.msgpack")
			await reply("данные удалены ^w^")
		except:
			await reply("не удалось удалить файлы")

	if command('/show'):
		if database_spisok.get(int(message.channel.id)):
			await reply(database_spisok.get(int(message.channel.id)))
		else:
			await reply("данных нет, введите id для подключения через /project (id проекта), ^w^")
	
	if command('/speak'):
		await reply("я бот для создания проектов на gitlab через дискорд созданный Артёмом (ака: TheRandomFurryGuy) и Богданом богом данным (ака: Zaboal) | [идея сделать меня фурри была предложена 1-м ради шутки]")
		await reply("====================================")
		await reply("список комманд которые я выполняю:\n/issue - создание задачи на gitlab\n/project - подключение id канала discord с id канала gitlab\n/remove - удаление id\n/show - показ id (к каждому каналу discord подключён отдельный id gitlab)\n/speak - я расскажу немного о себе (что сейчас и делаю)")

discord_bot.run(str(environ.get("TOKEN_DISCORD"))) # авторизация бота по токену из среды и запуск