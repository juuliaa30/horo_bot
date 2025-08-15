import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *
from parsing import get_capicorn

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

MENU, OPTION1, OPTION2 = range(3)

async def start_command(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Козерог', callback_data='option1')],
        [InlineKeyboardButton('Водолей', callback_data='option2')],
        [InlineKeyboardButton('Рыбы', callback_data='option3')],
        [InlineKeyboardButton('Овен', callback_data='option4')],
        [InlineKeyboardButton('Телец', callback_data='option5')],
        [InlineKeyboardButton('Близнецы', callback_data='option6')],
        [InlineKeyboardButton('Рак', callback_data='option7')],
        [InlineKeyboardButton('Лев', callback_data='option8')],
        [InlineKeyboardButton('Дева', callback_data='option9')],
        [InlineKeyboardButton('Весы', callback_data='option10')],
        [InlineKeyboardButton('Скорпион', callback_data='option11')],
        [InlineKeyboardButton('Стрелец', callback_data='option12')],
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text('Welcome! Please choose an option:', reply_markup=reply_markup)
    return MENU

async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "option1":
        await query.edit_message_text(text=get_capicorn())
        return OPTION1
    elif query.data == "option2":
        await query.edit_message_text(text="You selected Option 2.")
        return OPTION2
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MENU: [CallbackQueryHandler(button)],
            OPTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    app.add_handler(conv_handler)

    app.run_polling(poll_interval=5)