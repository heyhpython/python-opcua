import asyncio
import websockets
import logging
import redis
import json

logger = logging.getLogger(__name__)


def trans(d: dict):
    data = {}
    while d.__len__() > 0:
        k, v = d.popitem()
        k = k.decode('utf-8')
        v = v.decode('utf-8')
        v = {"True": True, "False": False}.get(v, v)
        data[k] = v
    return data


def from_redis():
    rdb = redis.StrictRedis.from_url('redis://localhost:6379/2')
    names = rdb.keys('*')
    ret = {}
    for name in names:
        data = {}
        try:
            content: dict = rdb.hgetall(name)
            content = trans(content)
            for k, v in content.items():
                levels = k.split('.')
                temp = data
                for l in levels:
                    # print("++++++ %s +++++" % l)
                    r = temp.get(l)
                    if not r:
                        temp[l] = {}
                    temp = temp[l]
                    # print(data)

                temp['val'] = v
            ret[name.decode('utf-8')] = data

        except Exception as e:
            logger.error(e)
            continue
    data = json.dumps(ret, ensure_ascii=False, indent=4)
    return data


async def echo(websocket, path):
    while 1:
        await websocket.send(from_redis())
        await asyncio.sleep(0.01)


if __name__ == '__main__':
    import ctypes

    server = websockets.serve(echo, '0.0.0.0', 12000)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()













