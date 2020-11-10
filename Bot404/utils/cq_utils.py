import aiocqhttp
from nonebot import get_bot
import traceback
import logging


def exception_handler(message='运行出现异常，请查看日志', log_level=logging.DEBUG, is_private=True, receiver=1135989508):
    # noinspection PyBroadException
    try:
        bot = get_bot()
        if is_private:
            if log_level == logging.DEBUG:
                logging.debug(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_private_msg(user_id=receiver, message=f'[Debug] {message}')
            elif log_level == logging.INFO:
                logging.info(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_private_msg(user_id=receiver, message=f'[Info] {message}')
            elif log_level == logging.WARNING:
                logging.warning(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_private_msg(user_id=receiver, message=f'[Warning] {message}')
            elif log_level == logging.ERROR:
                logging.error(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_private_msg(user_id=receiver, message=f'[Error] {message}')
            elif log_level == logging.CRITICAL:
                logging.critical(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_private_msg(user_id=receiver, message=f'[Critical] {message}')
        else:
            if log_level == logging.DEBUG:
                logging.debug(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_group_msg(group_id=receiver, message=f'[Debug] {message}')
            elif log_level == logging.INFO:
                logging.info(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_group_msg(group_id=receiver, message=f'[Info] {message}')
            elif log_level == logging.WARNING:
                logging.warning(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_group_msg(group_id=receiver, message=f'[Warning] {message}')
            elif log_level == logging.ERROR:
                logging.error(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_group_msg(group_id=receiver, message=f'[Error] {message}')
            elif log_level == logging.CRITICAL:
                logging.critical(f"{message}\n{traceback.format_exc()}")
                bot.sync.send_group_msg(group_id=receiver, message=f'[Critical] {message}')
    except aiocqhttp.exceptions.ActionFailed:
        logging.error(f"{message}\n{traceback.format_exc()}")
    except Exception:
        logging.critical(f"{message}\n{traceback.format_exc()}")


def send_message_sync(session, message):
    # noinspection PyBroadException
    try:
        bot = get_bot()
        if session.event.message_type == 'private':
            # noinspection PyBroadException
            try:
                bot.sync.send_private_msg(user_id=session.event.user_id, message=message)
            except Exception:
                logging.error(f'未能成功发送私聊消息：未知错误，请查看日志\n{session.event.user_id} <- {message}')
        elif session.event.message_type == 'group':
            # noinspection PyBroadException
            try:
                bot.sync.send_group_msg(group_id=session.event.group_id, message=message)
            except aiocqhttp.exceptions.ActionFailed:
                exception_handler(f'未能成功发送群消息：账号可能被风控\n{session.event.group_id} <- {message}', logging.WARNING)
            except Exception:
                exception_handler(f'未能成功发送群消息：未知错误，请查看日志\n{session.event.group_id} <- {message}', logging.ERROR)
        else:
            # noinspection PyBroadException
            try:
                bot.sync.send_discuss_msg(discuss_id=session.event.discuss_id, message=message)
            except aiocqhttp.exceptions.ActionFailed:
                exception_handler(f'未能成功发送讨论组消息：账号可能被风控\n{session.event.discuss_id} <- {message}', logging.WARNING)
            except Exception:
                exception_handler(f'未能成功发送讨论组消息：未知错误，请查看日志\n{session.event.discuss_id} <- {message}', logging.ERROR)
    except Exception:
        logging.critical(f"{message}\n{traceback.format_exc()}")


async def send_message_async(session, message):
    # noinspection PyBroadException
    try:
        await session.send(message)
    except aiocqhttp.exceptions.ActionFailed:
        exception_handler(f'未能成功发送异步消息：账号可能被风控\n{session.event.group_id} <- {message}', logging.WARNING)
    except Exception:
        exception_handler(f'未能成功发送异步消息：未知错误，请查看日志\n{session.event.group_id} <- {message}', logging.ERROR)
