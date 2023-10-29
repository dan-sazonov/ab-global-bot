from aiogram import types
import messages

_kb_on_voting = [
    [
        types.KeyboardButton(text="1"),
        types.KeyboardButton(text="2"),
    ],
]

keyboard_voting = types.ReplyKeyboardMarkup(
    keyboard=_kb_on_voting,
    resize_keyboard=True,
    input_field_placeholder=messages.KB_VOTING_PH
)
