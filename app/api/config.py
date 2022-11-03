import redis

redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0, password='admin', decode_responses=True)


def get_redis():
    return redis.Redis(connection_pool=redis_pool)
