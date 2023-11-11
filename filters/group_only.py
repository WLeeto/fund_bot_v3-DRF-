from aiogram import Router, types
from aiogram.filters import Filter
from aiogram.types import Message

from create_bot import registeredgroup_req

router = Router()


class GroupOnly(Filter):
    def __init__(self, msg: types.Message) -> None:
        self.user_id = msg.from_user.id
        self.group_id = msg.chat.id

    async def __call__(self, message: Message) -> bool:
        if self.user_id != self.group_id:
            return True