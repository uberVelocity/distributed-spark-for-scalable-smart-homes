from sensor import Sensor
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


if __name__ == '__main__':
    watt_params = {
        'a': 0.25,
        'b': 40,
        'variance': 0.1,
        'limit': 50
    }

    lumen_params = {
        'a': -2.5,
        'b': 500,
        'variance': 0.1,
        'limit': 400,
    }

    producer = None
    while not producer:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['kafka:29091'],
                key_serializer=lambda m: str(m).encode(),  # transforms id string to bytes
                value_serializer=lambda m: dumps(m).encode('ascii')  # transforms messages to json bytes
            )
        except NoBrokersAvailable:
            print('No brokers available, sleeping', flush=True)
            sleep(5)

    lamp = Sensor(watt_params, lumen_params)

    t = 0
    while True:
        if t == 50 or not lamp.on:   # break when appliance is broken or enough time has passed
            break

        timestamp = datetime.utcnow().timestamp()
        wattage = lamp.compute_var1(t)
        lumen = lamp.compute_var2(t)

        print(f"Device {lamp.id}: time({t}) = {timestamp}", flush=True)
        print(f"Device {lamp.id}: wattage({t}) = {wattage}")
        print(f"Device {lamp.id}: lumen({t}) = {lumen}")

        msg = {
            'id': lamp.id,
            'timestamp': timestamp,
            'sensors': {
                'lumen': lumen,
                'wattage': wattage,
            }
        }

        # Stream data and and sleep for 4 seconds between update.
        producer.send('sensor_data', key=lamp.id, value=msg).add_callback(on_send_success).add_errback(on_send_error)
        t += 1
        sleep(4)
