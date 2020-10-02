import aiocqhttp
from nonebot import get_bot
import traceback
import logging


def _cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


def exception_handler(message='运行出现异常，请查看日志', log_level=logging.DEBUG, is_private=True, receiver=1135989508):
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
        try:
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
            exception_handler(f'未能成功发送群消息：账号可能被风控\n{receiver} <- {message}', logging.WARNING)
        except Exception:
            exception_handler(f'未能成功发送群消息：未知错误，请查看日志\n{receiver} <- {message}', logging.ERROR)


def send_message_auto(session, message):
    bot = get_bot()
    if session.event.message_type == 'private':
        bot.sync.send_private_msg(user_id=session.event.user_id, message=message)
    elif session.event.message_type == 'group':
        try:
            bot.sync.send_group_msg(group_id=session.event.group_id, message=message)
        except aiocqhttp.exceptions.ActionFailed:
            exception_handler(f'未能成功发送群消息：账号可能被风控\n{session.event.group_id} <- {message}', logging.WARNING)
        except Exception:
            exception_handler(f'未能成功发送群消息：未知错误，请查看日志\n{session.event.group_id} <- {message}', logging.ERROR)
    else:
        try:
            bot.sync.send_discuss_msg(discuss_id=session.event.discuss_id, message=message)
        except aiocqhttp.exceptions.ActionFailed:
            exception_handler(f'未能成功发送讨论组消息：账号可能被风控\n{session.event.discuss_id} <- {message}', logging.WARNING)
        except Exception:
            exception_handler(f'未能成功发送讨论组消息：未知错误，请查看日志\n{session.event.discuss_id} <- {message}', logging.ERROR)
