from appliance import Appliance
from time import sleep
from datetime import datetime

if __name__ == '__main__':
    watt_params = {
        'base': 20,
        'variance': 0.2,
        'limit': 24
    }

    temp_params = {
        'base': 110,
        'variance': 0.2,
        'limit': 120,
        't_fault': 30
    }

    lamp = Appliance(watt_params, temp_params)

    t = 0
    while True:
        if t is 50 or lamp.on_state is False:
            break

        dt = datetime.utcnow().timestamp()
        watts = lamp.compute_wattage(t)
        temperature = lamp.compute_temperature(t)
        print(f"Device {lamp.id}: time({t}) = {dt}")
        print(f"Device {lamp.id}: wattage({t}) = {watts}")
        print(f"Device {lamp.id}: temperature({t}) = {temperature}")

        # Stream data and and sleep for 4 seconds between updates
        # TODO stream data per variable to ingestion service
        t += 1
        sleep(4)
