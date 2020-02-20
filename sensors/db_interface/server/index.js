const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const PackageService = require("../services/PackageService");
const {Kafka} = require('kafkajs')


const app = express();

const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['kafka:9092', 'kafka2:9092', 'kafka3:9092']
});

const consumer = kafka.consumer({groupId: 'db-interface'});

const run = async() => {
    await consumer.connect()
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


run().catch(console.error);

app.use(bodyParser.json());
app.use(cors());
app.use(express.json());

const insert = require('../routes/api/insert');

app.use('/api/insert', insert);

const port = process.env.PORT || 4004;

app.listen(port, () => console.log(`Test sensor started on port ${port}`));