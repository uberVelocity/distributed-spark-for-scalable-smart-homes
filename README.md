# Scalable households - Group 09 - SC

## Running the code
For now we have a data production and consumption demo. This can be ran using:

```shell script
docker-compose build --no-cache
docker-compose up
```

`sensor_heater` will produce updates for the simulated appliance. These are passed to Kafka and then consumed by
either the `db_interface` or the `test_consumer`.

## System Architecture
Please find the google slides describing our system architecture [here](https://docs.google.com/presentation/d/1NYL6EoNU3GWoOIYkiPU1ZjK3Hhs6i2bgwzrqqKD7PlU/edit?usp=sharing).



## Frontend

#### TODO:

- [ ] Interactive [map](https://leafletjs.com) with pins that simulate households. Click on a pin and be presented with options: view data (historical query) / request lifetime of appliances of household ([leaflet for Vue](https://www.npmjs.com/package/vue2-leaflet)).
- [ ] View data as [interactive/dynamic](https://www.chartjs.org) graphs.
- [ ] If no time for leaflet, a list of all households would suffice.