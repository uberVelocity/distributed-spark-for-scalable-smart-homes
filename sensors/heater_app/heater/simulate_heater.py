from heater import Heater
from time import sleep
from datetime import datetime
from json import dumps


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

    heater = Heater(watt_params, temp_params)

    t = 0
    while True:
        if t is 50 or heater.on_state is False:
            break

        timestamp = datetime.utcnow().timestamp()
        watts = heater.compute_wattage(t)
        temperature = heater.compute_heater(t)

        print(f"Device {heater.id}: time({t}) = {timestamp}")
        print(f"Device {heater.id}: wattage({t}) = {watts}")
        print(f"Device {heater.id}: temperature({t}) = {temperature}")

        update = {
            'id': heater.id,
            'timestamp': timestamp,
            'sensors': {
                'temperature': temperature,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between updates
        dumps(update)          # TODO stream data per variable to ingestion service

        t += 1
        sleep(4)
