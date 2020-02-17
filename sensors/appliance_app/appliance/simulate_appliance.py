from appliance import Appliance
from time import sleep
from datetime import datetime

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

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

    dev_id = 1
    device = Appliance(dev_id, watt_params, temp_params)
    
    t = 0
    while True:
        if t is 50 or device.on_state is False:
            break

        # TODO generate a timestamp that adheres to the UNIX Epoch https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date
        dt = datetime.now()
        watts = device.compute_wattage(t)
        temperature = device.compute_temperature(t)
        print(f"Device {device.id}: time({t}) = {dt}")
        print(f"Device {device.id}: wattage({t}) = {watts}")
        print(f"Device {device.id}: temperature({t}) = {temperature}")

        # Stream data and and sleep for 4 seconds between updates
        # TODO stream data per variable to ingestion service
        t += 1
        sleep(4)
