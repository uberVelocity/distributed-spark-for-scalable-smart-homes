import math
import random

from datetime import datetime


class Lamp:
    def __init__(self, watt_params, lumen_params):
        """
        Constructor which specifies the lamp sensor params.
        :param watt_params: Dict consisting of 'base' and 'variance' values.
        :param lumen_params: Dict consisting of 'base, 'variance' and 't_fault' values.
        """
        self.id = datetime.utcnow().timestamp()  # Use UNIX timestamp as temp id value
        self.on_state = True
        self.wattage_vars = watt_params
        self.lumen_vars = lumen_params

    def compute_wattage(self, t):
        jitter = (random.random() * 2 * self.wattage_vars['variance']) - self.wattage_vars['variance']

        time_to_wattage = math.pow(20, t/16) / 1750

        wattage = self.wattage_vars['base'] + time_to_wattage + jitter

        if wattage >= self.wattage_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return wattage

    def compute_lumen(self, t):
        jitter = (random.random() * 2 * self.lumen_vars['variance']) - self.lumen_vars['variance']

        time_to_lumen = 0
        if t > self.lumen_vars['t_fault']:
            time_to_lumen = t / (self.lumen_vars['base'] / 30)

        lumen = self.lumen_vars['base'] + time_to_lumen + jitter

        if lumen >= self.lumen_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return lumen
