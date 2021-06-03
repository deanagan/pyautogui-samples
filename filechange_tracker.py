import time
import datetime
from itertools import cycle



def check(status = None):
    # Using cycle to range infinitely
    for _ in cycle(range(10)):
        with open('file_to_track.txt', 'r') as tt:
            for line in tt:
                if status != line:
                    status = line
                    print("New Status: ", status)
                    print("Time Logged: ", datetime.datetime.now())
                break
        # sleep 1 second
        time.sleep(1)

check()