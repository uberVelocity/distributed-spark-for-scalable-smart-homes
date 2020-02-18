const express = require('express');
const router = express.Router();
const PackageService = require("../../services/PackageService");

// Handling random test values 
router.post('/test', async (req, res) => {
    const randomConsumption = req.body.data;
    console.log(`Random Consumption: ${randomConsumption}`);
    PackageService.consumeRandom(randomConsumption);
    res.status(201).send();
});

module.exports = router;