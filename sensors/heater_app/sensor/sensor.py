import random

from datetime import datetime


class Sensor:
    def __init__(self, var1, var2):
        """
        Constructor which specifies the sensor sensor params.
        :param var1: Dict consisting of 'base' and 'variance' values.
        :param var2: Dict consisting of 'base, 'variance' and 't_fault' values.
        """
        self.id = datetime.utcnow().timestamp()  # Use UNIX timestamp as temp id value
        self.on = True
        self.var1 = var1
        self.var2 = var2

    def compute_var1(self, t):
        if not self.on:
            return -1

        jitter = (random.random() * 2 * self.var1['variance']) - self.var1['variance']

        var1 = self.var1['a'] * t + self.var1['b'] + jitter

        if var1 >= self.var1['limit']:
            self.on = False  # If limit exceeded, break device
            return -1

        return var1

    def compute_var2(self, t):
        if not self.on:
            return -1

        jitter = (random.random() * 2 * self.var2['variance']) - self.var2['variance']

        var2 = self.var2['a'] * t + self.var2['b'] + jitter

        if var2 <= self.var2['limit']:
            self.on = False  # If limit exceeded, break device
            return -1

        return var2
