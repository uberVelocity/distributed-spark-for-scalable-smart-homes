const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const PackageService = require("../services/PackageService");
const {Kafka} = require('kafkajs')


const app = express();

setTimeout(() => {

    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: ['kafka:29092', 'kafka2:29092', 'kafka3:29092']
    });

    const consumer = kafka.consumer({groupId: 'db-interface'});

    const run = async() => {
        await consumer.connect()
        console.log(`connected to ${kafka.PORT}`)
        await consumer.subscribe({topic: 'historical', fromBeginning: true});
        
        await consumer.run({
            eachMessage: async ({topic, partition, message}) => {
                // For each message, you might want to insert it into the db.
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                })
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
