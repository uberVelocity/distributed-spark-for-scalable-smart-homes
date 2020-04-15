const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use(express.json());

const status = require('./routes/api/status');

app.use('/api/status', status);

const port = process.env.PORT || 3005;

app.listen(port, () => console.log(`Status retriever started on port ${port}`));
