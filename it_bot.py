from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token 
import logging, sqlite3, time

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# Реализация База данных на sqlite3
connection  = sqlite3.connect('itbot.db')
cursor = connection.cursor()
cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    date_joined VARCHAR(100)
);
""")

cursor.execute(f"""CREATE TABLE IF NOT EXISTS lids(
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    direction VARCHAR(100),
    phone VARCHAR(100),
    tg_user VARCHAR(255),
    created VARCHAR (100)
);
""")

start_keyboard = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('Заявка на курсы'),
    types.KeyboardButton('Рассылка')
]
start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    print(message)
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    output_cursor = cursor.fetchall()
    print(output_cursor)
    if output_cursor == []:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (
            message.from_user.id, message.from_user.first_name,
            message.from_user.last_name, message.from_user.username, time.ctime()
        ))
        cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_button)

@dp.message_handler(commands='id')
async def get_id(message:types.Message):
    await message.answer(f"{message.from_user.full_name} id {message.from_user.id}")
        
class MailingState(StatesGroup):
    text = State()
        
@dp.message_handler(text="Рассылка")  
async def start_mailing(message:types.Message):
    if message.from_user.id in [6505811922,]:
        await message.answer("Введите свой текст для рассылки")
        await MailingState.text.set()
    else:
        await message.answer("У вас нет прав для данного действия")
        
@dp.message_handler(state=MailingState.text)  
async def send_mailing(message:types.Message, state:FSMContext):
    await message.reply("Начинаю рассылку...")
    cursor.execute("SELECT id FROM users;")
    all_users_ids = cursor.fetchall()
    print(all_users_ids)
    for user_id in all_users_ids:
        await bot.send_message(user_id[0], message.text)
    await message.answer("Рассылка окончена")
    await state.finish()
    
@dp.message_handler(text='О нас')
async def about_us(message:types.Message):
    await message.reply("Geeks - это айти курсы в Бишкеке, Кара-Балте, Оше и в Ташкенте!")
    
@dp.message_handler(text='Адрес') 
async def send_address(message:types.Message): 
    await message.reply(f"Наш адрес Аматов 1Б!") 
    await message.answer_location(40.51931603792678, 72.80298388177104) 
 
courses_keyboard = [ 
    types.KeyboardButton('Backend'), 
    types.KeyboardButton('Frontend'), 
    types.KeyboardButton('Android'), 
    types.KeyboardButton('IOS'), 
    types.KeyboardButton('UX/UI'), 
    types.KeyboardButton('Назад') 
] 
courses_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_keyboard) 
         
@dp.message_handler(text='Курсы') 
async def send_courses(message:types.Message): 
    await message.reply(f"Вот наши курсы:", reply_markup=courses_button) 
    
@dp.message_handler(text="Backend") 
async def backend(message:types.Message): 
    await message.reply("Backend - это внутреняя часть сайта или приложения. \nСрок обучения 5 месяцев \nСтоимость: 10000 KGS в месяц")
    
@dp.message_handler(text="Frontend") 
async def backend(message:types.Message):


    await message.reply("Frontend - это внешняя часть сайта или приложения. \nСрок обучения 3 месяцa \nСтоимость: 10000 KGS в месяц")
    
@dp.message_handler(text="Android") 
async def backend(message:types.Message): 
    await message.reply("Android - создает приложения для устройств на операционной системе Android. \nСрок обучения 7 месяцев \nСтоимость: 10000 KGS в месяц")
 
@dp.message_handler(text="IOS") 
async def backend(message:types.Message): 
    await message.reply("IOS - создаёт и поддерживает различные приложения для операционной системы iOS.\ nСрок обучения 7 месяцев \nСтоимость: 10000 KGS в месяц")
    
@dp.message_handler(text="UX/UI") 
async def backend(message:types.Message): 
    await message.reply("UX/UI - это проектирование удобных, понятных и эстетичных пользовательских интерфейсов. \nСрок обучения 3 месяцa \nСтоимость: 10000 KGS в месяц")    

#Заявка на курсы кнопка
class LidsState(StatesGroup):
    first_name = State()
    last_name = State()
    direction = State()
    phone = State()
    
@dp.message_handler(text="Заявка на курсы") 
async def start_lids(message:types.Message): 
    await message.answer(f"{message.from_user.full_name} чтобы оставить заявку заполните поля")
    await message.answer("Как: Имя, Фамилия, Направление, Номер")
    await message.answer("Введите свое имя:")
    await LidsState.first_name.set()
    
@dp.message_handler(state=LidsState.first_name) 
async def get_last_name(message:types.Message, state:FSMContext): 
    await state.update_data(first_name=message.text)
    await message.answer("Введите фамилию:")
    await LidsState.last_name.set()
    
@dp.message_handler(state=LidsState.last_name) 
async def get_direction(message:types.Message, state:FSMContext): 
    await state.update_data(last_name=message.text)
    await message.answer("Введите направление:")
    await LidsState.direction.set()
    
@dp.message_handler(state=LidsState.direction) 
async def get_phone(message:types.Message, state:FSMContext): 
    await state.update_data(direction=message.text)
    await message.answer("Введите номер телефона:")
    await LidsState.phone.set()
    
@dp.message_handler(state=LidsState.phone) 
async def get_phone(message:types.Message, state:FSMContext): 
    await state.update_data(phone=message.text)
    await message.answer("сохраню данные...")
    result = await storage.get_data(user=message.from_user.id)
    print(result)

    cursor.execute("INSERT INTO lids VALUES (?,?,?,?,?,?);",
                  (result['first_name'], result['last_name'],
                   result ['direction'], result ['phone'],
                   f"{message.from_user.id} {message.from_user.username}",
                   time.ctime()) )
    cursor.connection.commit()
    await message.answer("данные записаны на базу")
    await state.finish()


@dp.message_handler(text='Назад') 
async def backroll(message:types.Message): 
    await start(message)
    
executor.start_polling(dp)

