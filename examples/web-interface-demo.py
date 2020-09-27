# import json
from fastapi import FastAPI, File, UploadFile

# Across Field
from starlette.middleware.cors import CORSMiddleware
# from typing import Optional
from pydantic import BaseModel

# Python WEB接口开发 Flask -> FastAPI
import logging
import time
import os
import json

# Add WEBAPP
app = FastAPI()

# Allow all
origins = [
    '*'
    # 如果需要解决跨域问题/访问拦截，可以在这里设置访问白名单（目前是全接受）
]

# Solver
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])
# Set Logger
logging.basicConfig(filename='runtime.log', level=logging.INFO)


@app.post('/bot')
async def funcname(group_id):
    return {
        'data': {
            'status': True
        }
    }


@app.post('/get_group_member_list')
async def funcname(group_id):
    return {
        'data': [
            'idk',
            'sth'
        ]
    }
