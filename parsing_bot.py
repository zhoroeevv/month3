from aiogram import Bot, Dispatcher, types, executor
from config import token
from bs4 import BeautifulSoup
import logging, requests

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands ='start')
async def hello(message:types.Message):
    await message.answer("привет, напиши /news для получение новостей")

@dp.message_handler(commands='news')
async def news(message:types.Message):
    await message.answer("отправляю новости...")

    number_news = 0
    for page in range(1,3):
        url = f'https://24.kg/page_{page}/'
        respone = requests.get(url=url)
        # print(respone)
        soup = BeautifulSoup(respone.text, 'lxml')
        # print(soup)
        all_news = soup.find_all('div', class_ ='title')
        # print(all_news)
        
        for news in all_news:
            number_news += 1
            # print(f"{number_news}) {news.text}")
            await message.answer(f"{number_news}) {news.text}")

executor.start_polling(dp, skip_updates=True)
