const localDatacenter = 'datacenter1';
const cassandra = require('cassandra-driver');
const contactPoints = ['cassandra-cluster', 'cassandra-cluster', 'cassandra-cluster'];
const loadBalancingPolicy = new cassandra.policies.loadBalancing.DCAwareRoundRobinPolicy(localDatacenter); 
const clientOptions = {
   policies : {
      loadBalancing : loadBalancingPolicy
   },
   contactPoints: contactPoints,
   authProvider: new cassandra.auth.PlainTextAuthProvider('cassandra', 'cassandra'),
   keyspace:'household'
};
let cassandraClient = new cassandra.Client(clientOptions);

const insertRandomQuery = 'INSERT INTO householdcompaction(appliance, ts, value) VALUES(?, ?, ?)';
module.exports = class PackageService {
    static async consumeRandom(randomConsumption) {
        const timeStamp = randomConsumption[0];
        const value = randomConsumption[1];
        const appliance = 'light bulb';  // To be replaced by actual appliance name

        const params = [appliance, timeStamp, value];
        PackageService.insertData(insertRandomQuery, params);
    }

    // Commit sensory data to Cassandra Cluster
    static async insertData(query, data) {
        // Commit data to Cassandra DB
        cassandraClient = new cassandra.Client(clientOptions);

        console.log(`attempting to insert ${data} using ${query}`);
        cassandraClient.execute(query, data, {prepare: true}, (err) => {
        if(err) {
            console.log(err);
        }
    });
  }
} 

