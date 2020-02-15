const express = require('express');
const StreamService = require("../services/StreamService");

const app = express();

const port = process.env.PORT || 3000;

// Generates test values.
async function generateValues() {

    // Generate random values for testing.
    const randomValue= Math.random();
    params = [new Date(), randomValue];
    console.log(`sending ${params[0]}:${randomValue}`);
    StreamService.streamData(params);
}

setInterval(generateValues, 4000);

app.listen(port, () => console.log(`Test sensor started on port ${port}`));