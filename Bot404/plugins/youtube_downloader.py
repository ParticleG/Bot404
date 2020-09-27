from nonebot import on_command, CommandSession
import youtube_dlc as yt_dlc


@on_command('ping')
async def ping(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    # city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 向用户发送天气预报
    await session.send(session.get('res'))


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@ping.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if not stripped_arg:
        session.state['res'] = "Pong!"
        return

    session.pause('Command: \"ping\" only support 0 argument.')
