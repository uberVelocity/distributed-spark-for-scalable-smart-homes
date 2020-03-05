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
                // For each message, you might want to insert it into the db.
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                
                const id = JSON.parse(message.value.toString())["id"];
                const ts = JSON.parse(message.value.toString())["timestamp"];
                const gw = JSON.parse(message.value.toString())["sensors"]["wattage"];
                const temp = JSON.parse(message.value.toString())["sensors"]["temperature"];
                params = [id, ts, gw, temp];
                console.log(`parameters to be inserted = ${params}`);


                // console.log(`params: [${id} ${ts} ${gw} ${temp}]`);
                // console.log('inserting message into cassandra');
                PackageService.insertData('heater', params);
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
