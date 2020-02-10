const express = require('express');
const mongodb = require('mongodb');
const dotenv = require('dotenv');

const StreamService = require("../services/StreamService");

const app = express();

dotenv.config();

const port = process.env.PORT || 3002;

// Generates Gw values
async function generateGw() {

    const servers = await getServersListFromMongo();
    // For each server in the server list, generate a gw consumption value
    if (servers.length > 0) {
        servers.forEach(server => {
            // Use server ID to INSERT value of gw and timestamp to corresponding servers
            const serverId = server._id.toString();
            const gwValue = Math.random();
            let params = [serverId, new Date(), gwValue];
            StreamService.streamData(params);
        });
    }
}

async function getServersListFromMongo() {
    const client = await mongodb.MongoClient.connect('mongodb://mongo-node:27017/admin', {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });

    const connection = client.db('admin').collection('servers');
    return connection.find({}).toArray();
}

// 'Read' Gw value every 4 seeconds
setInterval(generateGw, 4000);


app.listen(port, () => console.log(`Gw sensor started on port ${port}`));