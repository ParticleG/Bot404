CONSTANTS = {
    'ENABLE_WEBDAV': False
}

PATHS = {
    'CQ_PATH': '/usr/go-cqhttp/quin33/',
    'BOT_PATH': '/usr/go-cqhttp/quin33/Bot404/',
    'CACHE_PATH': '/usr/go-cqhttp/quin33/caches/',
    'WEBDAV_PATH': '/usr/webdav/holoen/',
    'DRIVE_PATH': '/usr/drive/holoen/'
}

GROUPS = [
    {
        'id': 'Fallback',
        'drive': f'{PATHS["DRIVE_PATH"]}/fallback',
        'group': None,
        'name': '缺省值',
        'nickname': '其他',
        'channel': None,
    },
    {
        'id': 'Kiara',
        'drive': f'{PATHS["DRIVE_PATH"]}/kiara',
        'group': 643815033,
        'name': '小鸟游琪亚娜',
        'nickname': '火鸡',
        'channel': 'UCHsx4Hqa-1ORjQTh9TYDhww',
    },
    {
        'id': 'Gura',
        'drive': f'{PATHS["DRIVE_PATH"]}/gura',
        'group': 901231107,
        'name': '噶呜古拉',
        'nickname': '鲨鱼',
        'channel': 'UCoSrY_IQQVpmIRZ9Xf-y93g',
    },
    {
        'id': 'Ina',
        'drive': f'{PATHS["DRIVE_PATH"]}/ina',
        'group': 203690749,
        'name': '一伊那尓栖',
        'nickname': '古神',
        'channel': 'UCMwGHR0BTZuLsmjY_NT5Pwg',
    },
    {
        'id': 'Calliope',
        'drive': f'{PATHS["DRIVE_PATH"]}/callio',
        'group': 826872326,
        'name': '森美声',
        'nickname': '死神',
        'channel': 'UCL_qhgtOy0dy1Agp8vkySQg',
    },
    {
        'id': 'Amelia',
        'drive': f'{PATHS["DRIVE_PATH"]}/amelia',
        'group': 829619725,
        'name': '阿米莉亚华生',
        'nickname': '侦探',
        'channel': 'UCyl1z3jo3XHR1riLFKG5UAg',
    }
]
