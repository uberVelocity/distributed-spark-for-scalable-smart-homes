from vacuum import Vacuum
from time import sleep
from datetime import datetime
from json import dumps
from kafka import KafkaProducer


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

    suction_params = {
        'base': 100,
        'variance': 2,
        'limit': 70,
        't_fault': 10
    }

    producer = KafkaProducer(
        bootstrap_servers=['kafka:29091'],
        key_serializer=lambda m: str(m).encode(),  # transforms id string to bytes
        value_serializer=lambda m: dumps(m).encode('ascii')  # transforms messages to json bytes
    )
    vacuum = Vacuum(watt_params, suction_params)

    t = 0
    while True:
        if t is 50 or vacuum.on_state is False:
            break

        timestamp = datetime.utcnow().timestamp()
        watts = vacuum.compute_wattage(t)
        suction = vacuum.compute_suction(t)

        print(f"Device {vacuum.id}: time({t}) = {timestamp}")
        print(f"Device {vacuum.id}: wattage({t}) = {watts}")
        print(f"Device {vacuum.id}: suction({t}) = {suction}")

        msg = {
            'id': vacuum.id,
            'timestamp': timestamp,
            'sensors': {
                'suction': suction,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between updates
        producer.send('historical', key=vacuum.id, value=msg).add_callback(on_send_success).add_errback(on_send_error)
        t += 1
        sleep(4)
