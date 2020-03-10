const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const PackageService = require("../services/PackageService");
const {Kafka} = require('kafkajs')


const app = express();

setTimeout(() => {

    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
    });

    const consumer = kafka.consumer({groupId: 'db-interface'});

    const run = async() => {
        await consumer.connect()
        console.log(`connected to ${kafka.PORT}`)
        await consumer.subscribe({topic: 'sensor_data', fromBeginning: true});
        
        await consumer.run({
            eachMessage: async ({topic, partition, message}) => {
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                let params;
                let sensor;
                const id = JSON.parse(message.value.toString())["id"];
                const ts = JSON.parse(message.value.toString())["timestamp"];
                const gw = JSON.parse(message.value.toString())["sensors"]["wattage"];
                
                if (message.value.toString().includes("temperature")) {
                    const temp = JSON.parse(message.value.toString())["sensors"]["temperature"];
                    params = [id, ts, gw, temp];
                    sensor = 'heater';
                    console.log(`Heater message to be inserted = ${params}`);
                }
                else if (message.value.toString().includes("lumen")) {
                    const lumen = JSON.parse(message.value.toString())["sensors"]["lumen"];
                    params = [id, ts, gw, lumen];
                    sensor = 'lamp';
                    console.log(`Lamp message to be inserted = ${params}`);
                }
                else if (message.value.toString().includes("suction")) {
                    const suction = JSON.parse(message.value.toString())["sensors"]["suction"];
                    params = [id, ts, gw, suction];
                    sensor = 'vacuum';
                    console.log(`Vacuum message to be inserted = ${params}`);
                }
                PackageService.insertData(sensor, params);
            }
        });
    }

    run();

    app.use(bodyParser.json());
    app.use(cors());
    app.use(express.json());

    const insert = require('../routes/api/insert');

    app.use('/api/insert', insert);

    const port = process.env.PORT || 4004;

    app.listen(port, () => console.log(`Test sensor started on port ${port}`));
}, 10000);
