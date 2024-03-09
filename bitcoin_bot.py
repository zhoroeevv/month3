from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, aioschedule, asyncio, requests
from time import ctime

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def get_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    btc_price = round(float(response.get('price')))
    return btc_price

async def get_eth_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
    response = requests.get(url=url).json()
    eth_price = round(float(response.get('price')))
    return eth_price

async def send_crypto_prices():
    btc_price = await get_btc_price()
    eth_price = await get_eth_price()

    await bot.send_message(-4000645080, f"BTC Цена: {btc_price} {ctime()}:")
    await bot.send_message(-4000645080, f"ETH Цена: {eth_price} {ctime()}:")

async def scheduler():
    while True:
        await send_crypto_prices()
        await asyncio.sleep(5)

async def on_startup(dispatcher):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

