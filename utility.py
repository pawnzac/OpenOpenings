from datetime import datetime
import time

def odd_or_even(x,y):
    if ((x % 2 == 0) & (y % 2 ==0)):
        return True

    if (((x % 2) == 1) & ((y % 2)==1)):
        return True

    return False

def compute_stats(x):
    all_time_tries = 0
    all_time_moves = 0
    last7_moves = 0
    last7_tries = 0
    last30_moves = 0
    last30_tries = 0
    last_practice = 0
    current_time = time.time()
    for t in x:
        all_time_tries += t['tries']
        all_time_moves += t['moves']
        if ((current_time-t['time']) < (7*24*60*60)):
            last7_tries += t['tries']
            last7_moves += t['moves']
        if ((current_time-t['time']) < (30*24*60*60)):
            last30_tries += t['tries']
            last30_moves += t['moves']

        if (t['time'] > last_practice):
            last_practice = t['time']

    fmt_lastprac = datetime.utcfromtimestamp(last_practice).strftime("%Y-%m-%d %H:%M:%S UTC")
    return {'All Time' : round(all_time_tries / all_time_moves,2),
            'Last Week': round(last7_tries/last7_moves,2),
            'Last 30 Days': round(last30_tries/last30_moves,2),
            'Last Practice': fmt_lastprac}


