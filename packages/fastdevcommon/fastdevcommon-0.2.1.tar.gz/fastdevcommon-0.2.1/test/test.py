import asyncio

from FastDevCommon import OperateResult

from FastDevCommon import AsyncRedisClient

redis_client = AsyncRedisClient(username="r-uf69w3hrd6eauou49g",password="jingda_8888",host="r-uf69w3hrd6eauou49gpd.redis.rds.aliyuncs.com",port=16379,db_num=0)

print(asyncio.run(redis_client.set("test",value="你好")))