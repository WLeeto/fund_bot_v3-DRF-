from aiogram import Bot
from aiogram import Dispatcher
from async_API.requests.requests import Profile, Group, RegisteredGroup, Transaction, ProfileGroup
from os import environ

token_tg = environ.get('TELEGRAM_TOKEN')
bot = Bot(token=token_tg)
dp = Dispatcher()

profile_req = Profile()
group_req = Group()
registeredgroup_req = RegisteredGroup()
transaction_req = Transaction()
profile_group_req = ProfileGroup()

