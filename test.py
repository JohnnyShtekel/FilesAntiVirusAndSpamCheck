from __future__ import absolute_import
from celery import Celery
import time

app = Celery('FilesAntiVirusAndSpamCheck',
             broker='amqp://guest:guest@localhost:5672//',
             backend='rpc://',
             include=['FilesAntiVirusAndSpamCheck.tasks'])





@app.task
def longtime_add(x, y):
    print 'long time task begins'
    # sleep 5 seconds
    time.sleep(5)
    print 'long time task finished'
    return x + y




if __name__ == '__main__':
    result = longtime_add.delay(1,2)
    # at this time, our task is not finished, so it will return False
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result
    # sleep 10 seconds to ensure the task has been finished
    time.sleep(10)
    # now the task should be finished and ready method will return True
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result