from aiogram import Dispatcher, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import ChatMember
from create_bot import dp, registeredgroup_req, group_req, profile_req, bot
from create_logger import logger
from misc.utils import register_new_group, register_new_user, register_user_if_not_exists, \
    register_group_with_validation, set_new_group_limit, create_new_transaction, \
    create_new_transaction_with_validations, register_user_group_with_validation, is_group_active
from texts.all_messages import errors, info
from pprint import pprint
from filters.group_is_active import GroupIsActive
from filters.group_only import GroupOnly


@dp.message(Command(commands=['r', 'x']))
async def r(msg: types.Message):
    print(msg)
    user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
    await msg.answer('Yo!')


# @dp.message(Command('start'))
async def start(msg: types.Message):
    if msg.chat.id != msg.from_user.id:
        await register_user_if_not_exists(msg)
        register_group = await register_group_with_validation(msg)
        if register_group:
            await register_user_group_with_validation(msg)
    else:
        await register_user_if_not_exists(msg)


# @dp.message(Command(commands=['sl', 'setlimit']))
async def setlimit(msg: types.Message):
    if msg.chat.id != msg.from_user.id:
        is_active = await is_group_active(msg.chat.id, msg)
        if is_active:
            await set_new_group_limit(msg)


# @dp.message(F.text.isdigit(), F.text != '0')
async def new_transaction(msg: types.Message):
    if msg.chat.id != msg.from_user.id:
        is_active = await is_group_active(msg.chat.id, msg)
        if is_active:
            if int(msg.text) > 0:
                await create_new_transaction_with_validations(msg)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(start, Command('start'))
    dp.message.register(setlimit, Command(commands=['sl', 'setlimit']))
    dp.message.register(new_transaction, F.text.isdigit(), F.text != '0')