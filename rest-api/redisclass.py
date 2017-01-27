# -*- coding: utf-8 -*-

import logging
import pika
import time
from threading import Thread
import redis
import json
import os

LOGGER = logging.getLogger(__name__)

class DBRedis(object):
    
    def __init__(self):
        self.rdb = redis.Redis(host=os.environ['DB_REDIS'], port=6379, db=0)

    def save_json(self,json_to_save, key):
        json_dump = json.dumps(json_to_save)
        self.rdb.set(key, json_dump)

    def get_json(self,key):
        LOGGER.info('key: '+key)
        LOGGER.info(self.rdb.get(key))
        return self.rdb.get(key)

