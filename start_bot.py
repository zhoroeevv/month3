from config import token 
from aiogram import Bot, Dispatcher, executor, types
bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет dfsafdsdfsdfss! Привет Geeks")

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("Чем я могу вам помочь?")

@dp.message_handler(text="Geeks")
async def geeks(message:types.Message):
    await message.reply("Geeks - это айти курсы в Кыргызстане")

@dp.message_handler(text="Привет")
async def hello(message:types.Message):
    await message.reply("Привет, как дела?")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.answer_photo('https://avatars.mds.yandex.net/get-vertis-journal/4469561/2019-09-09-3550e6211d984b0887cb89e09ce7c137.jpg_1622735908352/orig')
    await message.answer_location(40.51936, 72.8027)

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял, введите /help")

executor.start_polling(dp)
