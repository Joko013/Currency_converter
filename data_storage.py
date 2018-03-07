import json
import time
import redis


class RedisStorage(object):
    """ Object for connecting to Redis server instance, used for saving and retrieving data. """

    def __init__(self):
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def get_data(self, key):
        """ Get [key] data from Redis server. """
        self._data = self._r.get(key)
        if self._data:
            data = json.loads(self._data)
        else:
            data = None
        return data

    def set_data(self, key, data, exp=None):
        """ Save [data] with a [key] and optional [exp] argument to specify expiration to Redis server. """

        self._r.set(key, json.dumps(data))
        if exp:
            self._r.expireat(key, int(time.mktime(exp.timetuple())))
        return data




