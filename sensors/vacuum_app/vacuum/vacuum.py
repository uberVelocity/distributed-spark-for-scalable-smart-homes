import math
import random

from datetime import datetime


class Vacuum:
    def __init__(self, watt_params, suction_params):
        """
        Constructor which specifies the vacuum sensor params.
        :param watt_params: Dict consisting of 'base' and 'variance' values.
        :param suction_params: Dict consisting of 'base, 'variance' and 't_fault' values.
        """
        self.id = datetime.utcnow().timestamp()  # Use UNIX timestamp as temp id value
        self.on_state = True
        self.wattage_vars = watt_params
        self.suction_vars = suction_params

    def compute_wattage(self, t):
        jitter = (random.random() * 2 * self.wattage_vars['variance']) - self.wattage_vars['variance']

        time_to_wattage = math.pow(2, t/4.8) / 100

        wattage = self.wattage_vars['base'] + time_to_wattage + jitter

        if wattage >= self.wattage_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return wattage

    def compute_suction(self, t):
        jitter = (random.random() * 2 * self.suction_vars['variance']) - self.suction_vars['variance']

        time_to_suction = 0
        if t > self.suction_vars['t_fault']:
            time_to_suction = t/1.4
            print(time_to_suction)

        suction = self.suction_vars['base'] - time_to_suction + jitter

        if suction <= self.suction_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return suction if suction < 100 else 100
