from lamp import Lamp
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
        'base': 6,
        'variance': 0.2,
        'limit': 10
    }

    lumen_params = {
        'base': 110,
        'variance': 0.2,
        'limit': 120,
        't_fault': 30
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
    lamp = Lamp(watt_params, lumen_params)

    t = 0
    while True:
        if t is 50 or lamp.on_state is False:
            break

        timestamp = datetime.utcnow().timestamp()
        watts = lamp.compute_wattage(t)
        lumen = lamp.compute_lumen(t)

        print(f"Device {lamp.id}: time({t}) = {timestamp}")
        print(f"Device {lamp.id}: wattage({t}) = {watts}")
        print(f"Device {lamp.id}: lumen({t}) = {lumen}")

        msg = {
            'id': lamp.id,
            'timestamp': timestamp,
            'sensors': {
                'lumen': lumen,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between updates
        producer.send('historical', key=lamp.id, value=msg).add_callback(on_send_success).add_errback(on_send_error)
        t += 1
        sleep(4)
