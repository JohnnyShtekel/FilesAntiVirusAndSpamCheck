import thread
from kombu import Connection
import datetime

def add_message():
    while True:
        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            simple_queue = conn.SimpleQueue('simple_queue')
            message = 'helloword, sent at %s' % datetime.datetime.today()
            simple_queue.put(message)
            print('Sent: %s' % message)
            simple_queue.close()


def get_message():
    while True:
        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            simple_queue = conn.SimpleQueue('simple_queue')
            message = simple_queue.get(block=True, timeout=1)
            print("Received: %s" % message.payload)
            message.ack()
            simple_queue.close()

# add_message()
# get_message()

try:
   thread.start_new_thread( add_message(), ("Thread-1", 2, ) )
   thread.start_new_thread( get_message, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass