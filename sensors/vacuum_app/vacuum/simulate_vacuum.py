from vacuum import Vacuum
from time import sleep
from datetime import datetime
from json import dumps


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

        update = {
            'id': vacuum.id,
            'timestamp': timestamp,
            'sensors': {
                'temperature': suction,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between updates
        dumps(update)          # TODO stream data per variable to ingestion service

        t += 1
        sleep(4)
