const {Kafka} = require('kafkajs')

const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
});

const consumer = kafka.consumer({groupId: 'status-retriever'});

module.exports = class KafkaController {
    
    static async getData() {
        await consumer.connect()
        await consumer.subscribe({topic: 'sensor_data', fromLatest: true});
        
        await consumer.run({
            eachMessage: async ({topic, partition, message}) => {
                console.log({
                    partition,
                    offset: message.offset,
                    value: message.value.toString(),
                });
                let params;
                let sensor;
                const data = JSON.parse(message.value.toString());
                
                const id = data["id"];
                const timestamp = data["timestamp"];
                const t = data["t"];
                const model = data["model"];
                const variables = data["variables"];

                if (model == "heater") {
                    const temp = variables["temperature"];
                    const wattage = variables["wattage"];
                    params = [id, model, t, timestamp, wattage, temp];
                    sensor = "heater";
                    console.log(`Heater message to be inserted = ${params}`);
                }
                else if (model == "lamp") {
                    const lumen = variables["lumen"];
                    const wattage = variables["wattage"];
                    params = [id, model, t, timestamp, wattage, lumen];
                    sensor = "lamp";
                    console.log(`Lamp message to be inserted = ${params}`);
                }
                else if (message == "vacuum") {
                    const suction = variables["suction"];
                    const wattage = variables["wattage"];
                    params = [id, model, t, timestamp, wattage, suction];
                    sensor = "vacuum";
                    console.log(`Vacuum message to be inserted = ${params}`);
                }
                consumer.disconnect();
                return params;
            }
        });
    }
}
