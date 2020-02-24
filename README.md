# 2020_group_09_s2534657_s3192423_s3083357

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
>>>>>>> 8b8d221975883fd1ed016685ede22b1a00fbcbaf
