from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# создаём Inline-кнопку с WebApp
main_but = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Открыть приложение', web_app=WebAppInfo(url="https://669a861a6cbb.ngrok-free.app"))]
])
