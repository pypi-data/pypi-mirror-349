#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2025/04/24 10:54:17
@Author  :   Yan Wen 
@Version :   1.0
@Contact :   z19040042@s.upc.edu.cn
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import uvicorn
from server import app, AppConfig  # noqa: F401


if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        root_path=AppConfig.app_root_path,
        reload=AppConfig.app_reload,
    )
