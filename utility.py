# OpenOpenings
# Copyright 2021 pawnzac <pawnzac90@gmail.com>

# This file is part of OpenOpenings.

# OpenOpenings is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# OpenOpenings is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with OpenOpenings.  If not, see <https://www.gnu.org/licenses/>.

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
    return {'All Time' : round(100*all_time_moves / all_time_tries,2),
            'Last Week': round(100*last7_moves/last7_tries,2),
            'Last 30 Days': round(100*last30_moves/last30_tries,2),
            'Last Practice': fmt_lastprac}


