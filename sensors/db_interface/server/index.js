const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const PackageService = require("../services/PackageService");

const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use(express.json());

const insert = require('../routes/api/insert');

app.use('/api/insert', insert);

const port = process.env.PORT || 4000;

app.listen(port, () => console.log(`Test sensor started on port ${port}`));