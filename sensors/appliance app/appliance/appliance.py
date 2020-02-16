import math
import random


class Appliance:
    def __init__(self, appliance_id, watt_params, temp_params):
        """
        Constructor which specifies the appliance sensor params.
        :param appliance_id: UUID.
        :param watt_params: Dict consisting of 'base' and 'variance' values.
        :param temp_params: Dict consisting of 'base, 'variance' and 't_fault' values.
        """
        self.id = appliance_id
        self.on_state = True
        self.wattage_vars = watt_params
        self.temp_vars = temp_params

    def compute_wattage(self, t):
        jitter = (random.random() * 2 * self.wattage_vars['variance']) - self.wattage_vars['variance']

        time_to_wattage = math.pow(20, t/16) / 1750

        wattage = self.wattage_vars['base'] + time_to_wattage + jitter

        if wattage >= self.wattage_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return wattage

    def compute_temperature(self, t):
        jitter = (random.random() * 2 * self.temp_vars['variance']) - self.temp_vars['variance']

        time_to_temp = 0
        if t > self.temp_vars['t_fault']:
            time_to_temp = t / (self.temp_vars['base'] / 30)

        temperature = self.temp_vars['base'] + time_to_temp + jitter

        if temperature >= self.temp_vars['limit']:
            self.on_state = False  # If limit exceeded, break device
            return -1

        return temperature
