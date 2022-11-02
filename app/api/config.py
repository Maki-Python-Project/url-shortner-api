from redis_om import get_redis_connection


redis_db = get_redis_connection(
    host='redis', port='6379'
)
