from appliance import Appliance
from time import sleep

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

    device = Appliance(watt_params, temp_params)

    t = 0
    while True:
        if t is 50 or device.on_state is False:
            break

        watts = device.compute_wattage(t)
        temperature = device.compute_temperature(t)

        print(f"Device {device.id}: wattage({t}) = {watts}")
        print(f"Device {device.id}: temperature({t}) = {temperature}")

        # Stream data and and sleep for 4 seconds between updates
        # TODO stream data per variable to ingestion service
        t += 1
        sleep(4)
