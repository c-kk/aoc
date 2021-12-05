import atexit
from time import time, strftime, localtime
from datetime import timedelta

def format(dif):
    sec = str(timedelta(seconds=dif))[:-4]
    if sec[0:6] == '0:00:0': sec = sec[6:] + "s"
    return sec    

def log(title="Time"):
    global sub
    sec = format(time() - sub)
    print(f'{title}: {sec}')
    sub = time()

def finish():
    sec = format(time() - start)
    print(f'Total: {sec}')

start = time()
sub   = start
atexit.register(finish)