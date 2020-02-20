from heater import Heater
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
        'base': 1500,
        'variance': 20,
        'limit': 2000
    }

    temp_params = {
        'base': 22,
        'variance': 0.2,
        'limit': 20,
        't_fault': 10
    }

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        key_serializer=lambda m: m.encode(),                 # transforms id string to bytes
        value_serializer=lambda m: dumps(m).encode('ascii')  # transforms messages to json bytes
    )
    heater = Heater(watt_params, temp_params)

    t = 0
    while True:
        if t is 50 or heater.on_state is False:   # break when appliance is broken or enough time has passed
            break

        timestamp = datetime.utcnow().timestamp()
        watts = heater.compute_wattage(t)
        temperature = heater.compute_heater(t)

        print(f"Device {heater.id}: time({t}) = {timestamp}")
        print(f"Device {heater.id}: wattage({t}) = {watts}")
        print(f"Device {heater.id}: temperature({t}) = {temperature}")

        msg = {
            'id': heater.id,
            'timestamp': timestamp,
            'sensors': {
                'temperature': temperature,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between update.
        producer.send('historical', key=heater.id, value=msg).add_callback(on_send_success).add_errback(on_send_error)
        t += 1
        sleep(4)
