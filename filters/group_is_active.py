from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

from create_bot import registeredgroup_req

router = Router()


class GroupIsActive(Filter):
    def __init__(self, group_id: int) -> None:
        self.group_id = group_id

    async def __call__(self, message: Message) -> bool:
        result = await registeredgroup_req.get_with_params({'group_tg_id': -4000756056, 'is_active': True})
        if result:
            return True