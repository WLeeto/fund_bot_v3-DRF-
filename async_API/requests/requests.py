import aiohttp

from create_logger import logger
from async_API.requests.requests_utils import logger_message

from os import environ

token_drf_bot = 'a6ffe1533c4ccd034be9b1fe28541913bf3d2b50'  # todo в переменные окружения (dev)
# token_drf_bot = environ.get('DRF_TOKEN')


class APIRequests:
    def __init__(self):
        self.headers = {
            "Authorization": f"Token {token_drf_bot}"
        }
        self.url = 'http://127.0.0.1:8000/api/'
        # self.url = environ.get('DRF_URL')

    async def get_all(self) -> list:
        """
        Get list of all profiles.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers, ssl=True) as response:
                logger.info(f'Sending GET to {self.url}')
                if response.status == 200:
                    logger_message('info', method='GET', url=self.url, headers=self.headers)
                    result = await response.json()
                    return result
                else:
                    logger_message('error', method='GET', url=self.url, headers=self.headers)
                    logger.error(await response.text())
                    return

    async def get_with_param(self, param_name: str, param_value: str) -> list:
        """

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}?{param_name}={param_value}', headers=self.headers, ssl=True) as response:
                logger.info(f'Sending GET to {self.url}?{param_name}={param_value}')
                if response.status == 200:
                    logger_message('info', method='GET', url=f'{self.url}?{param_name}={param_value}',
                                   headers=self.headers)
                    result = await response.json()
                    return result
                else:
                    logger_message('error', method='GET', url=f'{self.url}?{param_name}={param_value}',
                                   headers=self.headers)
                    logger.error(await response.text())
                    return

    async def get_with_params(self, params_dict: dict) -> list:
        """
        Recives { 'param_name': param_value, }
        """
        url = f'{self.url}?'
        for key, value in params_dict.items():
            url += f'{key}={value}&'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, ssl=True) as response:
                logger.info(f'Sending GET to {url}')
                if response.status == 200:
                    logger_message('info', method='GET', url=f'{url}',
                                   headers=self.headers)
                    result = await response.json()
                    return result
                else:
                    logger_message('error', method='GET', url=f'{self.url}?{url}',
                                   headers=self.headers)
                    logger.error(await response.text())
                    return

    async def post(self, **kwargs):
        """
        Creates POST request.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=kwargs.get('body')) as response:
                logger.info(f'Sending POST to {self.url}')
                if response.status == 201:
                    logger_message('info', method='POST', url=f'{self.url}', headers=self.headers,
                                   body=kwargs.get('body'))
                    return await response.json()
                else:
                    logger_message('error', method='POST', url=f'{self.url}', headers=self.headers,
                                   body=kwargs.get('body'))
                    logger.error(await response.text())
                    return

    async def patch(self, **kwargs):
        """
        Creates patch request.
        """
        url = f'{self.url}{kwargs.get("id")}/'
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=self.headers, json=kwargs.get('body')) as response:
                logger.info(f'Sending PATCH to {url}')
                if response.status == 200:
                    logger_message('info', method='PATCH', url=url, headers=self.headers, body=kwargs.get('body'))
                    return await response.json()
                else:
                    logger_message('error', method='PATCH', url=url, headers=self.headers, body=kwargs.get('body'))
                    logger.error(await response.text())
                    return


class Profile(APIRequests):
    def __init__(self):
        super().__init__()
        self.empty = self.url
        self.url = self.url + 'profile/'

    async def register_new_user(self, **kwargs):
        url = self.empty + 'register-from-bot/'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=kwargs.get('body')) as response:
                logger.info(f'Sending POST to {url}')
                if response.status == 201:
                    logger_message('info', method='POST', url=url, headers=self.headers, body=kwargs.get('body'))
                    return await response.json()
                else:
                    logger_message('error', method='POST', url=url, headers=self.headers, body=kwargs.get('body'))
                    logger.error(await response.text())
                    return


class Group(APIRequests):
    def __init__(self):
        super().__init__()
        self.url = self.url + 'group/'


class RegisteredGroup(APIRequests):
    def __init__(self):
        super().__init__()
        self.url = self.url + 'registeredgroup/'


class Transaction(APIRequests):
    def __init__(self):
        super().__init__()
        self.empty = self.url
        self.url = self.url + 'transaction/'

    async def get_amount_by_group_from_week_start(self, group_tg_id):
        """
        Gets total amount of transactions in current week by group.
        """
        url = f'{self.empty}get-week-transactions/?group_id={group_tg_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                logger.info(f'Sending POST to {url}')
                if response.status == 200:
                    logger_message('info', method='POST', url=url, headers=self.headers)
                    return await response.json()
                else:
                    logger_message('error', method='POST', url=url, headers=self.headers)
                    logger.error(await response.text())
                    return


class ProfileGroup(APIRequests):
    def __init__(self):
        super().__init__()
        self.url = self.url + 'profilegroup/'
