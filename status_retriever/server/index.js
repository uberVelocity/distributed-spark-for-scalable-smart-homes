const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const {Kafka} = require('kafkajs');
const ResultService = require('./services/ResultService');

const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use(express.json());

const status = require('./routes/api/status');

app.use('/api/status', status);

const port = process.env.PORT || 3005;

setTimeout(() => {
    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
    });
    
    const consumer = kafka.consumer({groupId: 'status-retriever'});

    const run = async() => {
        await consumer.connect();
        await consumer.subscribe({topic: 'sensor_data', fromBeginning: false});
        await consumer.run({
            eachMessage: async ({topic, partition, message}) => {
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                const data = JSON.parse(message.value.toString());
                
                const id = data["id"];
                const model = data["model"];
                console.log(`id: ${id}, model: ${model}`);
                const params = [id, model];
                ResultService.insertPrediction(params);
            }
        });
    }

    run();

    app.listen(port, () => console.log(`Status retriever started on port ${port}`));
}, 10000);





