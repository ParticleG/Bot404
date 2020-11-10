CONSTANTS = {
    'ENABLE_WEBDAV': False
}

PATHS = {
    'CQ_PATH': '/usr/go-cqhttp/quin33/',
    'BOT_PATH': '/usr/go-cqhttp/quin33/Bot404/',
    'CACHE_PATH': '/usr/go-cqhttp/quin33/caches/',
    'WEBDAV_PATH': '/usr/webdav/holoen/',
    'DRIVE_PATH': '/usr/drive/'
}

GROUPS = [
    {
        'id': 'Fallback',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/fallback',
        'group': None,
        'type': 'normal',
        'name': '缺省值',
        'nickname': '其他',
        'channel': None,
    },
    {
        'id': 'Kiara',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/kiara',
        'group': 643815033,
        'type': 'translate',
        'name': '小鸟游琪亚娜',
        'nickname': '火鸡',
        'channel': 'UCHsx4Hqa-1ORjQTh9TYDhww',
    },
    {
        'id': 'Gura',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/gura',
        'group': 901231107,
        'type': 'translate',
        'name': '噶呜古拉',
        'nickname': '鲨鱼',
        'channel': 'UCoSrY_IQQVpmIRZ9Xf-y93g',
    },
    {
        'id': 'Ina',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/ina',
        'group': 203690749,
        'type': 'translate',
        'name': '一伊那尓栖',
        'nickname': '古神',
        'channel': 'UCMwGHR0BTZuLsmjY_NT5Pwg',
    },
    {
        'id': 'Calliope',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/callio',
        'group': 826872326,
        'type': 'translate',
        'name': '森美声',
        'nickname': '死神',
        'channel': 'UCL_qhgtOy0dy1Agp8vkySQg',
    },
    {
        'id': 'Amelia',
        'drive': f'{PATHS["DRIVE_PATH"]}/holoen/amelia',
        'group': 829619725,
        'type': 'translate',
        'name': '阿米莉亚华生',
        'nickname': '侦探',
        'channel': 'UCyl1z3jo3XHR1riLFKG5UAg',
    },
    {
        'id': 'HoloEN',
        'drive': None,
        'group': 1083488442,
        'type': 'translate',
        'name': 'STEA总群',
        'nickname': 'STEA',
        'channel': None,
    },
    {
        'id': 'Alice',
        'drive': f'{PATHS["DRIVE_PATH"]}/nijisanji/alice',
        'group': 700976506,
        'type': 'translate',
        'name': '物述有栖',
        'nickname': '爱丽丝',
        'channel': 'UCt0clH12Xk1-Ej5PXKGfdPA',
    },
    {
        'id': 'Alice_work',
        'drive': f'{PATHS["DRIVE_PATH"]}/nijisanji/alice',
        'group': 958474641,
        'type': 'translate',
        'name': '物述有栖',
        'nickname': '爱丽丝',
        'channel': 'UCt0clH12Xk1-Ej5PXKGfdPA',
    },
    {
        'id': 'STEA',
        'drive': None,
        'group': 628669530,
        'type': 'code',
        'name': 'STEA总群',
        'nickname': 'STEA',
        'channel': None,
    },
]
