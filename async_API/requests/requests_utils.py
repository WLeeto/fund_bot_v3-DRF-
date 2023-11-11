from create_logger import logger


def logger_message(message_type: str, **kwargs) -> None:
    """
    Creates logger info massage.
    """
    method = kwargs.get('method')
    url = kwargs.get('url')
    headers = kwargs.get('headers')
    body = kwargs.get('body')
    if message_type == 'info':
        logger.info(f'{method} to {url} with headers: {headers} and body: {body}')
    elif message_type == 'error':
        logger.error(f'{method} to {url} with headers: {headers} and body: {body}')
    else:
        logger.warning(f'{method} to {url} with headers: {headers} and body: {body}')