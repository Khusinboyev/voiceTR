from aiogram import *
from handlers.users.start_handler import *
from handlers.admin.admin_handlers import *
from key import bot, dp
from deep_translator import GoogleTranslator
from googletrans import Translator
from keyboards.buttons import main_btn, main_btn2, main_btn1, main_btn3, main_btn4
from gtts import gTTS
translatorg = Translator()


class functions:
	@staticmethod
	async def check_on_start(user_id):
		with connect('./database/database.sqlite3') as db:
			cursor = db.cursor()
			rows = cursor.execute("SELECT id from channels ").fetchall()
			error_code = 0
			for row in rows:
				r = await bot.get_chat_member(chat_id=row[0], user_id=user_id)
				if r.status in ['member', 'creator', 'admin']:
					pass
				else:
					error_code = 1
		if error_code == 0:
			return True
		else:
			return False

@dp.message_handler(commands=['help'])
async def qr(message:types.Message):
	await message.reply('Assalomu alaykum 👋\nBu bot sizga matnlarni tarjima qilishda yordam beradi.\n Tarjima tilini almashtirish uchun /lang buyrug`idan foydalaning\nBiror narsaga tushunmasangiz va bot uchun g`oya yoki taklif bo`lsa adminga murojaat qiling @coder_admin')


@dp.message_handler(commands=['lang'])
async def choosLang(message: types.Message):
	await message.reply('Tilni Tilni almashtirishingiz mumkin', reply_markup=main_btn)


""""""""""""""""""""""""""""""""""""""""""'''til tanlash'''""""""

@dp.message_handler(text = ['UZ - EN', '✅ UZ - EN'])
async def translete(message: types.Message):
	file = open(f"txt/{message.from_user.id}.txt", "w")
	file.write('UZ - EN')
	file.close()
	await message.reply('🇺🇿UZ - 🇬🇧EN tili tanlandi\n\n\nTarjima tilini almashtirish uchun /lang buyrug`idan foydalaning', reply_markup=main_btn1)


@dp.message_handler(text = ['UZ - RU', '✅ UZ - RU'])
async def translete(message: types.Message):
	file1 = open(f"txt/{message.from_user.id}.txt", "w")
	file1.write('UZ - RU')
	file1.close()
	await message.reply('🇺🇿UZ - 🇷🇺RU tili tanlandi\n\n\nTarjima tilini almashtirish uchun /lang buyrug`idan foydalaning', reply_markup=main_btn2)

@dp.message_handler(text = ['🎧 Audio🇷🇺', '✅ 🎧 Audio🇷🇺'])
async def translete(message: types.Message):
	file1 = open(f"txt/{message.from_user.id}.txt", "w")
	file1.write('Audioru')
	file1.close()
	await message.reply('🎧 Audio  tanlandi\n\n\nTarjima tilini almashtirish uchun /lang buyrug`idan foydalaning', reply_markup=main_btn3)

@dp.message_handler(text = ['🎧 Audio🇺🇸', '✅ 🎧 Audio🇺🇸'])
async def translete(message: types.Message):
	file1 = open(f"txt/{message.from_user.id}.txt", "w")
	file1.write('Audioen')
	file1.close()
	await message.reply('🎧 Audio  tanlandi\n\n\nTarjima tilini almashtirish uchun /lang buyrug`idan foydalaning', reply_markup=main_btn4)


@dp.message_handler(content_types='text')
async def translete(message: types.Message):
	if await functions.check_on_start(message.chat.id):
		try:
			lang = translatorg.detect(message.text).lang
			id = message.from_user.id
			file2 = open(f"txt/{id}.txt", "r+")
			til = file2.read()
			if til == 'UZ - EN':
				print(til)
				if lang == 'uz':
					translator = GoogleTranslator(source='uz', target='en')
					await message.reply(translator.translate(message.text))
				else:
					translator = GoogleTranslator(source='auto', target='uz')
					await message.reply(translator.translate(message.text))
			elif til == 'UZ - RU':
				print(til)
				if lang == 'uz':
					translator = GoogleTranslator(source='uz', target='ru')
					await message.reply(translator.translate(message.text))
				else:
					translator = GoogleTranslator(source='auto', target='uz')
					await message.reply(translator.translate(message.text))
			elif til == 'Audioen':
				print(til)
				send = await message.answer('⏳')
				await asyncio.sleep(1)
				await bot.delete_message(chat_id=message.chat.id, message_id=send.message_id)
				id = message.from_user.id
				text = message.text
				tts = gTTS(text, lang='en')
				tts.save(f'audio/{id}.mp3')
				await message.answer_audio(audio=open(f'audio/{id}.mp3', 'rb'))
			elif til == 'Audioru':
				print(til)
				send = await message.answer('⏳')
				await asyncio.sleep(1)
				await bot.delete_message(chat_id=message.chat.id, message_id=send.message_id)
				id = message.from_user.id
				text = message.text
				tts = gTTS(text, lang='ru')
				tts.save(f'audioru/{id}.mp3')
				await message.answer_audio(audio=open(f'audioru/{id}.mp3', 'rb'))
		except FileNotFoundError:
				await message.reply('Tilni tanlang /lang')
	else:
		await message.reply(f'Assalomu alaykum {message.from_user.first_name}\nBotimizdan foydalanish uchun kanalimizga azo bo`ing👇👇', reply_markup=join_inline)

if __name__=='__main__':
	executor.start_polling(dispatcher=dp)