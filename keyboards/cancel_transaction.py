from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class CancelTransactionCallbackFactory(CallbackData, prefix='c_t'):
    action: str
    value: int


def cancel_transaction_kb(buttons_data: list):
    builder = InlineKeyboardBuilder()
    for button in buttons_data:
        builder.button(
            text=f'Сумма:{button["amount"]} / Дата:{button["transaction_date"]}',
            callback_data=CancelTransactionCallbackFactory(action=f'{button["amount"]}', value=button['id'])
        )
    builder.adjust(1)
    return builder.as_markup()