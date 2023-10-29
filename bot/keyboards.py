from aiogram import types
import messages

kb_on_start = [
    [
        types.KeyboardButton(text=messages.KB_START_TEXT),
    ],
]

keyboard_start = types.ReplyKeyboardMarkup(
    keyboard=kb_on_start,
    resize_keyboard=True,
    input_field_placeholder=messages.KB_START_PH
)
