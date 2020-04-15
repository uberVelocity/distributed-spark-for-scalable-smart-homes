const router = require("express").Router();
const KafkaService = require('../../services/kafkaController');

// Post to http://statusretriever:3005/api/status
router.post('/', (req, res) => {
    const predictions = KafkaService.getData();
    console.log(`predictions: ${predictions}`);
    res.json({predictions}).status(200).send();
});

module.exports = router;
