import nonebot
import config
import logging
from os import path
from nonebot.log import logger
import logging
if __name__ == '__main__':
    nonebot.init(config)
<<<<<<< HEAD
    bot = nonebot.get_bot()
    # logger.setLevel(logging.WARNING)
    bot.logger.setLevel(logging.WARNING)
=======
    nonebot.get_bot().logger.setLevel(logging.WARNING)
>>>>>>> Particle_G
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'Bot404', 'plugins'),
        'Bot404.plugins'
    )
    nonebot.run()
