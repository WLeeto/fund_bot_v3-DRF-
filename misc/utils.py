import datetime

from aiogram import types
from aiogram.enums import ChatMemberStatus

from create_bot import group_req, profile_req, registeredgroup_req, transaction_req, profile_group_req, bot
from create_logger import logger
from texts.all_messages import info, errors
from aiogram.methods import SetMyCommands


async def set_default_commands():
    """

    """
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начать работу"),
        types.BotCommand(command="balance", description="Узнать текущий баланс"),
    ])


async def register_new_group(msg: types.Message) -> None:
    """
    Register new group.
    """
    body = {
        'group_tg': msg.chat.id,
        'group_name': msg.chat.title,
    }
    result = await group_req.post(body=body)
    if result:
        await msg.answer(info['group_has_been_registered'])
    else:
        await msg.answer(errors['cant_register_group'])


async def register_new_user(msg: types.Message) -> None:
    """
    Register new user.
    """
    body = {
        'username': msg.from_user.username,
        'tg_id': msg.from_user.id,
        'tg_name': msg.from_user.username,
        'name': msg.from_user.first_name,
        'surname': msg.from_user.last_name
    }

    result = await profile_req.register_new_user(body=body)

    if result:
        text = info['user_has_been_registered'].format(login=result.get('username'),
                                                       password=result.get('password'))
        await msg.answer(text)
    else:
        await msg.answer(info['cant_register_user'])


async def register_user_if_not_exists(msg: types.Message) -> None:
    """
    Check if user in db. Register new user if not.
    """
    is_user = await profile_req.get_with_param('tg_id', msg.from_user.id)
    if not is_user:
        await register_new_user(msg)
    else:
        await msg.answer(info['user_already_registered'])


async def register_group_with_validation(msg: types.Message) -> bool:
    """
    Validete group is active. Validate group is not register. Register new group.
    """
    await msg.answer(info['your_group_id'].format(group_id=msg.chat.id))
    registered_group = await registeredgroup_req.get_with_params({
        'group_tg_id': msg.chat.id,
        'is_active': True,
    })

    if registered_group:
        if await group_req.get_with_param('group_tg', msg.chat.id):
            await msg.answer(info['group_already_registered'])
        else:
            await register_new_group(msg)
        return True
    else:
        await msg.answer(errors['not_in_registeredgroup'])
        return False


async def set_new_group_limit(msg: types.Message) -> None:
    """
    Set new group_limit parametr with validations.
    """
    try:
        int(msg.text.split(' ')[1])
    except ValueError:
        await msg.answer(errors['int_requiered'])
        return

    group = await group_req.get_with_param('group_tg', msg.chat.id)
    if group:
        result = await group_req.patch(id=group[0].get('id'), body={'week_limit': msg.text.split(' ')[1]})
        if result:
            await msg.answer(info['week_limit_changed'].format(new_limit=msg.text.split(' ')[1]))
        else:
            await msg.answer(errors['cant_set_new_limit'])
    else:
        await msg.answer(errors['group_is_not_registered'])


async def create_new_transaction_with_validations(msg: types.Message):
    """

    """
    user = await profile_req.get_with_param('tg_id', msg.from_user.id)
    if not user:
        await msg.answer(errors['user_not_registered'])
        return
    group = await group_req.get_with_param('group_tg', msg.chat.id)
    if not group:
        await msg.answer(errors['group_not_registered'])
        return
    result = await create_new_transaction(user[0]['id'], group[0]['id'], msg.text)
    if result:
        await msg.answer(info['transaction_success'].format(amount=msg.text))
    else:
        await msg.answer(errors['cant_create_transaction'])


async def create_new_transaction(profile_id: int, group_id: int, amount: int) -> None:
    """
    Creates new transaction.
    """
    body = {
        'profile_id': profile_id,
        'group_id': group_id,
        'amount': amount,
    }
    return await transaction_req.post(body=body)


async def register_user_group_with_validation(msg: types.Message) -> None:
    """

    """
    admin = False
    user_type = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
    if user_type.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        admin = True
    profile = await profile_req.get_with_param('tg_id', msg.from_user.id)
    if not profile:
        await msg.answer(errors['user_not_registered'])
        return
    group = await group_req.get_with_param('group_tg', msg.chat.id)
    if not group:
        await msg.answer(errors['group_not_registered'])
    await register_user_group(profile[0]['id'], group[0]['id'], admin)


async def register_user_group(profile_id: int, group_id: int, is_admin: bool) -> None:
    """

    """
    body = {
        'profile_id': profile_id,
        'group_id': group_id,
        'is_admin': is_admin,
    }
    await profile_group_req.post(body=body)


async def is_group_active(group_id: int, msg: types.Message) -> bool:
    """
    Check if telegram group active.
    """
    result = await registeredgroup_req.get_with_params({'group_tg_id': group_id, 'is_active': True})
    if result:
        return True
    else:
        await msg.answer(errors['group_is_not_active'])
        return False


def get_monday_date() -> datetime.date:
    """
    Get date of monday in current week.
    """
    today = datetime.date.today()
    week_day = today.weekday()
    days_to_monday = 0 - week_day
    return today + datetime.timedelta(days=days_to_monday)


async def get_amount_of_all_transactions_for_group(msg: types.Message) -> dict:
    """
    Returns amount of all transaction in msg. group of the week.
    """
    returned_dict = await transaction_req.get_amount_by_group_from_week_start(msg.chat.id)
    return returned_dict