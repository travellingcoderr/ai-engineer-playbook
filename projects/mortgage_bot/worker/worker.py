import os
from redis import Redis
from rq import Worker, Queue

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    # Pass the connection directly to the Queues and the Worker
    queues = [Queue(name, connection=conn) for name in listen]
    worker = Worker(queues, connection=conn)
    worker.work()
