const {Kafka} = require('kafkajs');

const kafka = new Kafka({
    clientId: 'my-third-app',
    brokers: ['kafka:29091', 'kafka2:29092', 'kafka3:29093']
});

var sensorDictionary = {}
var latestCoefficients = {
    a: null,
    b: null,
    lim: null
}
function insertSensorData(sensorData){
    sensorDictionary[sensorData.id] = sensorData;
    if(latestCoefficients.a != null){
        produceMessage(sensorData.id);
    }
    else{
        console.log("No coefficients received yet... :(");
    }
}

function insertCoefficients(coefficients){
    latestCoefficients = coefficients;
    produceMessage();
}

async function produceMessage(specificSensor){
    messages = [];
    sensorIds = [];
    if(specificSensor){
        sensorIds.push(specificSensor);
    }
    else {
       for(var key in sensorDictionary.keys()){
        sensorIds.push(key);
       } 
    }
    for(var sensorId in sensorIds){
        var messageValue = {};
        deltaT = (latestCoefficients.lim - latestCoefficients.b)/latestCoefficients.a - sensorDictionary[id].t;
        messageValue = {
            id: sensorId,
            deltat: deltaT
        };
        messages.push({value: messageValue});
    }
    var producer = kafka.producer();
    console.log(messages);
    await producer.connect();
    await producer.send({
        topic: "predictions",
        messages: messages
    })
    await producer.disconnect();
}

module.exports = {
    insertSensorData: insertSensorData,
    insertCoefficients: insertCoefficients
}