from lamp import Lamp
from time import sleep
from datetime import datetime
from json import dumps

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

        update = {
            'id': lamp.id,
            'timestamp': timestamp,
            'sensors': {
                'lumen': lumen,
                'wattage': watts,
            }
        }

        # Stream data and and sleep for 4 seconds between updates
        dumps(update)          # TODO stream data per variable to ingestion service

        t += 1
        sleep(4)
