import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Подключение к базе данных
conn = sqlite3.connect('video_games.db')
cursor = conn.cursor()

# Создание таблицы для хранения информации о видеоиграх
cursor.execute('''
CREATE TABLE IF NOT EXISTS video_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    release_year INTEGER,
    developer TEXT,
    rating REAL
)
''')

# Добавление нескольких записей в таблицу
games = [
    ('The Witcher 3: Wild Hunt', 'Action RPG', 2015, 'CD Projekt Red', 9.2),
    ('Horizon Zero Dawn', 'Action RPG', 2017, 'Guerrilla Games', 8.9),
    ('Cyberpunk 2077', 'Action RPG', 2020, 'CD Projekt Red', 7.5),
    ('God of War', 'Action Adventure', 2018, 'Santa Monica Studio', 9.5),
    ('The Legend of Zelda: Breath of the Wild', 'Action Adventure', 2017, 'Nintendo', 9.8),
    ('Red Dead Redemption 2', 'Open World Action-Adventure', 2018, 'Rockstar Games', 9.7),
    ('DOOM Eternal', 'First Person Shooter', 2020, 'id Software', 8.5),
    ('Spider-Man: Miles Morales', 'Superhero Action-Adventure', 2020, 'Insomniac Games', 8.8),
    ('Star Wars Jedi: Fallen Order', 'Third-person action-adventure', 2019, 'Respawn Entertainment', 8.3),
    ('Resident Evil Village', 'Survival Horror', 2021, 'Capcom', 8.6)
]

cursor.executemany('INSERT INTO video_games (title, genre, release_year, developer, rating) VALUES (?, ?, ?, ?, ?)', games)

# Сохранение изменений
conn.commit()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Введи свой возраст.")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    
    # Проверка, является ли сообщение возрастом
    if message.isdigit():
        age = int(message)
        if age < 18:
            await update.message.reply_text("Ты еще слишком молод! Иди делать уроки.")
        else:
            # Создание клавиатуры с выбором игр
            keyboard = [
                [InlineKeyboardButton("The Witcher 3: Wild Hunt", callback_data='The Witcher 3: Wild Hunt')],
                [InlineKeyboardButton("Horizon Zero Dawn", callback_data='Horizon Zero Dawn')],
                [InlineKeyboardButton("Cyberpunk 2077", callback_data='Cyberpunk 2077')],
                [InlineKeyboardButton("God of War", callback_data='God of War')],
                [InlineKeyboardButton("The Legend of Zelda: Breath of the Wild", callback_data='The Legend of Zelda: Breath of the Wild')],
                [InlineKeyboardButton("Red Dead Redemption 2", callback_data='Red Dead Redemption 2')],
                [InlineKeyboardButton("DOOM Eternal", callback_data='DOOM Eternal')],
                [InlineKeyboardButton("Spider-Man: Miles Morales", callback_data='Spider-Man: Miles Morales')],
                [InlineKeyboardButton("Star Wars Jedi: Fallen Order", callback_data='Star Wars Jedi: Fallen Order')],
                [InlineKeyboardButton("Resident Evil Village", callback_data='Resident Evil Village')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Выбери игру:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Введи свой возраст.")

# Обработчик выбора игры
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    game_title = query.data
    
    cursor.execute('SELECT * FROM video_games WHERE title = ?', (game_title,))
    result = cursor.fetchone()
    
    if result:
        await query.answer()
        await query.edit_message_text(f"Название: {result[1]}\nЖанр: {result[2]}\nГод выпуска: {result[3]}\nРазработчик: {result[4]}\nРейтинг: {result[5]}")
    else:
        await query.answer()
        await query.edit_message_text("Игра не найдена.")

# Создание и запуск бота
def main() -> None:
    application = Application.builder().token('7634165625:AAHAEm0czIzXKxpF9jDUuUePm11xVVeH_IA').build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()

if __name__ == '__main__':
    main()