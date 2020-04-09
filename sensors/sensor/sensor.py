import random

from time import sleep
from datetime import datetime
from json import dumps
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def on_send_success(metadata):
    print(metadata.topic)
    print(metadata.partition)
    print(metadata.offset)


def on_send_error(excp):
    print(f'I am an errback {excp}')
    # handle exception


class Sensor:
    def __init__(self, variables):
        """
        Constructor which specifies the sensor sensor params.
        :param variables: list of the Variable namedtuple.
        """
        self.id = datetime.utcnow().timestamp()  # Use UNIX timestamp as temp id value
        self.on = True
        self.variables = variables
        self.producer = None

        while not self.producer:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=['kafka:29091'],
                    key_serializer=lambda m: str(m).encode(),  # transforms id string to bytes
                    value_serializer=lambda m: dumps(m).encode('ascii')  # transforms messages to json bytes
                )
            except NoBrokersAvailable:
                print('No brokers available, sleeping', flush=True)
                sleep(5)

    def compute_variable(self, variable, t):
        """
        Computes the corresponding variable value given a iteration t.
        :param variable: namedtuple Variable containing variable parameters.
        :param t: iteration to be calculated for.
        :return: value for variable at iteration t.
        """
        if not self.on:
            return -1

        jitter = (random.random() * 2 * variable.variance) - variable.variance
        next_value = variable.a * t + variable.b + jitter

        if next_value >= variable.limit:
            self.on = False  # If limit exceeded, break device
            return -1

        return next_value

    def run_simulation(self):
        """
        Runs the simulation for the sensor using the parameters set at creation. Sends an update to
        a Kafka ingestion service every 4 seconds until the sensor breaks.

        :return:
        """
        t = 0
        while True:

            # Break when appliance is broken or enough time has passed
            if t == 50 or not self.on:
                break

            # Get update timestamp
            timestamp = datetime.utcnow().timestamp()
            print(f"Device {self.id}: time({t}) = {timestamp}", flush=True)

            # For each variable of the sensor, compute the next value
            sensor_dict = {}
            for variable in self.variables:
                next_value = self.compute_variable(variable, t)
                sensor_dict[variable.name] = next_value
                print(f"Device {self.id}: " + variable.name + f"({t}) = {next_value}")

            # Create message dict containing all relevant data
            msg = {
                'id': self.id,
                'timestamp': timestamp,
                'sensors': sensor_dict
            }

            # Stream data and and sleep for 4 seconds between update.
            self.producer.send('sensor_data', key=self.id, value=msg).add_callback(on_send_success).add_errback(
                on_send_error)
            t += 1
            sleep(4)


