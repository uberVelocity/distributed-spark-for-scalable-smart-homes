const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const {Kafka} = require('kafkajs');

const StreamHandler = require('./../services/StreamHandler.js');

const app = express();
setTimeout(() => {

    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
    });

    const sensorConsumer = kafka.consumer({groupId: 'sensor-consumer'});

    const runSensorConsumer = async() => {
        await sensorConsumer.connect()
        await sensorConsumer.subscribe({topic: 'sensor_data', fromBeginning: false});
        
        await sensorConsumer.run({
            eachMessage: async ({topic, partition, message}) => {
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                const id = JSON.parse(message.value.toString())["id"];
                const t = JSON.parse(message.value.toString())["t"];
                let sensorData = {id, t}
                StreamHandler.insertSensorData(sensorData);
            }
        });

    }

    const kafka2 = new Kafka({
        clientId: 'my-second-app',
        brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
    });

    const coeffConsumer = kafka2.consumer({groupId: 'coeff-consumer'});

    const runCoeffConsumer = async() => {
        await coeffConsumer.connect()
        await coeffConsumer.subscribe({topic: 'coefficients', fromBeginning: false});
        
        await coeffConsumer.run({
            eachMessage: async ({topic, partition, message}) => {
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                const a = JSON.parse(message.value.toString())["a"];
                const b = JSON.parse(message.value.toString())["b"];
                const lim = JSON.parse(message.value.toString())["lim"];
                
                let coefficients = {a, b, lim}
                StreamHandler.insertCoefficients(coefficients);
            }
        });

    }

    runSensorConsumer();
    runCoeffConsumer();

    app.use(bodyParser.json());
    app.use(cors());
    app.use(express.json());

    const port = process.env.PORT || 4005;

    app.listen(port, () => console.log(`Node streaming started on port ${port}`));
}, 10000);
