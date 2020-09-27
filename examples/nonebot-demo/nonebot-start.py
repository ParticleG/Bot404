import nonebot
from os import path

'''
nonebot封装的CQHTTP插件
'''

if __name__ == "__main__":
    nonebot.init()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()
