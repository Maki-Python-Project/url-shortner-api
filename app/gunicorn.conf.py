from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


loglevel = 'info'
max_requests = 1000
workers = max_workers()
bind = '0.0.0.0:8000'
accesslog = errorlog = '/home/log/gunicorn/prod.log'
