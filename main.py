import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *
from parsing import get_horo

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

MENU, HORO = range(2)

BUTTONS = [
        [InlineKeyboardButton('Козерог', callback_data='capricorn')],
        [InlineKeyboardButton('Водолей', callback_data='aquarius')],
        [InlineKeyboardButton('Рыбы', callback_data='pisces')],
        [InlineKeyboardButton('Овен', callback_data='aries')],
        [InlineKeyboardButton('Телец', callback_data='taurus')],
        [InlineKeyboardButton('Близнецы', callback_data='gemini')],
        [InlineKeyboardButton('Рак', callback_data='cancer')],
        [InlineKeyboardButton('Лев', callback_data='leo')],
        [InlineKeyboardButton('Дева', callback_data='virgo')],
        [InlineKeyboardButton('Весы', callback_data='libra')],
        [InlineKeyboardButton('Скорпион', callback_data='scorpio')],
        [InlineKeyboardButton('Стрелец', callback_data='sagittarius')],
    ]

ZODIAC_SIGNS = {
    'capricorn', 'aquarius', 'pisces', 'aries',
    'taurus', 'gemini', 'cancer', 'leo',
    'virgo', 'libra', 'scorpio', 'sagittarius'
}

def get_keyboard():
    return InlineKeyboardMarkup(BUTTONS)

async def start_command(update: Update, context: CallbackContext):
    reply_markup = get_keyboard()

    await update.message.reply_text('Выберите Ваш знак зодиака', reply_markup=reply_markup)
    return MENU

async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    reply = [[InlineKeyboardButton('Назад', callback_data='back')]]
    await query.answer()

    if query.data == 'back':
        await query.edit_message_text(text='Выберите Ваш знак зодиака', reply_markup=get_keyboard())
        return MENU

    if query.data not in ZODIAC_SIGNS and query.data != 'back':
        await query.answer("Неизвестный знак зодиака")
        return

    await query.edit_message_text(text=get_horo(query.data), reply_markup=InlineKeyboardMarkup(reply))

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Я не понимаю.\nПожалуйста, выберите из списка', reply_markup=get_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MENU: [CallbackQueryHandler(button)],
            HORO: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.run_polling(poll_interval=5)