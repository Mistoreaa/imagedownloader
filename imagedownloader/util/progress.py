

import sys
import math


class Progress():

    max_gauge = 40

    def __init__(self):
        pass

    def set_max(self, max):
        self.max = max

    def show(self, increment):
        rate, count = self.__get_rate(increment)
        percentage = math.ceil(rate * 100)
        gauge = self.__build_gauge(count)
        #lf = '\n' if rate == self.max_gauge else ''
        lf = ''
        val = '\rprogress: {0}:[{1}%]{2}'.format(''.join(gauge), percentage, lf)
        sys.stdout.write(val)

    def __get_rate(self, increment):
        rate = round(increment / self.max, 2)
        count = math.ceil(self.max_gauge * rate)
        return rate, count

    def __build_gauge(self, count):
        gauge = [' '] * self.max_gauge
        if count:
            for i in range(count):
                gauge[i] = '#'
        return gauge
