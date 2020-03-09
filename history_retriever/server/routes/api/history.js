const express = require('express');
const router = express.Router();

const localDatacenter = 'datacenter1';
const cassandra = require('cassandra-driver');
const contactPoints = ['cassandra-cluster', 'cassandra-cluster', 'cassandra-cluster'];
const loadBalancingPolicy = new cassandra.policies.loadBalancing.DCAwareRoundRobinPolicy(localDatacenter); 

const clientOptionsHousehold = {
   policies : {
      loadBalancing : loadBalancingPolicy
   },
   contactPoints: contactPoints,
   authProvider: new cassandra.auth.PlainTextAuthProvider('admin', 'q1w2e3r4'),
   keyspace:'household'
};

const getHeaterInfo = 'SELECT id, ts, gw, temp FROM heatersensor';
const getVacuumInfo = 'SELECT id, ts, gw, suction FROM vacuumsensor';
const getLampInfo = 'SELECT id, ts, gw, lumen FROM lampsensor;'

// Get history of heater
router.get('/heater', async (req, res) => {
    console.log(`retrieving heater history`);
    const heaterHistory = await compileServerListWithHistory('heater');
    res.status(200).send(heaterHistory);
});

// Get history of vacuum
router.get('/vacuum', async (req, res) => {
    const vacuumHistory = await compileServerListWithHistory('vacuum');
    res.status(200).send(vacuumHistory);
});

// Get history of lamp
router.get('/lamp', async (req, res) => {
    const lampHistory = await compileServerListWithHistory('lamp');
    res.status(200).send(lampHistory);
});

// Compiles and returns a list of values of a certain property (either CO2 or GW)
// with timestamps from Cassandra FOR ALL SERVERS THAT ARE CURRENTLY IN MONGO (so not ones that have values)
// but have been removed from the database
async function compileServerListWithHistory(requestType) {
    cassandraClient = new cassandra.Client(clientOptionsHousehold);
    const sensor = requestType;
    switch(requestType) {
        case 'heater':
            requestType = getHeaterInfo;
            break;
        case 'vacuum':
            requestType = getVacuumInfo;
            break;
        case 'lamp':
            requestType = getLampInfo;
            break;
        default:
            return err;
    }
    let compiledList = [];

    await new Promise((resolve, reject) => {
        cassandraClient.execute(requestType, (result, err) => {
            if(err) {
                reject(err);
            }
            let newHistory = {
                ids: err.rows[0].id,
                ts: err.rows[0].ts,
                gw: err.rows[0].gw,
                values: ''
            }
            
            console.log(`hardcoded 0 row: ${err.rows[0].id}`);
            console.log(`$KEYS OF HISTORY: ${Object.keys(newHistory)}`);
            switch(sensor) {
                case 'heater':
                    newHistory.values = err.rows[0].temp;
                    break;
                case 'vacuum':
                    newHistory.values = err.rows[0].suction;
                    break;
                case 'lamp':
                    newHistory.values = err.rows[0].lumen;
                    break;
                default:
                    console.log('err00');
                    return err;
            }
            console.log(`new history: ${newHistory}`);
            compiledList.push(newHistory);
            resolve()
        })
    }).then(
        response => {},
        reason => {}
    );
    
    return compiledList;
}

module.exports = router;