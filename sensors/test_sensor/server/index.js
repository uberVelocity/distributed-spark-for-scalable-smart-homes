const express = require('express');
const StreamService = require("../services/StreamService");

const app = express();

const port = process.env.PORT || 3002;

// Generates test values.
async function generateValues() {

    // Generate random values for testing.
    const randomValue= Math.random();
    params = [new Date(), randomValue];
    StreamService.streamData(params);
}

app.listen(port, () => console.log(`Test sensor started on port ${port}`));