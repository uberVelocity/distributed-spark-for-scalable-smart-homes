# Household appliances lifetime predictions
The following application monitors the status of appliances within a household and predicts the remaining lifetime of each appliance. 

<!-- Each comment should be explained 'briefly'. -->

### Data
<!-- Simulated data -->

### Sensors
<!-- Python Docker containers that can be deployed to increase load -->

<!-- Different types of sensors -->

<!-- Mathematical functions that the sensors implement -->

<!-- Breaking behaviour of sensor and how this is represented (-1) -->

### Database 
<!-- Type of database used (NoSQL CassandraDB) -->
CassandraDB was the NoSQL database of choice in order to fascilitate horizontal scalability and storing fast time-series data.

<!-- Advantages of using said database -->
Due to the fact that CassandraDB uses SSTables with consistent hashing, reading on one particular row is very fast.

<!-- Replicability strategy -->
Each instance of Cassandra uses a replication factor of 3 per created table.
<!-- Compaction -->
A compaction strategy is implemented per each table.

<!-- Interface of Database -->
As sensors send historical data through Kafka, a service layer that ingests the data and abstracts accessibility to the database was created. With this, sensors do not have direct access to the database and the rate at which data is inserted into the database can be controlled. 

<!-- What do you store in it (what tables, historical data) -->
The database contains a keyspace `household` that has three tables, one for each type of sensor that store historical data, and one `predictions` table that stores the results of our model.  

<!-- Initialization of database -->
The tables are created automatically during its initialization through the use of the `cassandra-init.sh` script.

### Message broker
<!-- Reasons for using Kafka w/ Zookeeper -->

<!-- Replicated brokers (there are three) -->

<!-- Topics created and why (who are producers / consumers) -->

<!-- Historical / Streaming data -->

### Computational layer
<!-- Spark cluster specification (historical train / streaming predict) -->

<!-- Spark node that submits application -->

<!-- Implementation of historical -->

<!-- Implementation of streaming -->


### Containerization
<!-- Docker containers -->
Every service has been containerized and managed using Docker and `docker-compose`.

<!-- Volumes used for Cassandra, Kafka, and Zookeeper -->
Separate volumes were created for containers that are stateful in nature (i.e. Cassandra, Kafka, and Zookeeper). Every service communicated with one another through a bridge network named `household-network`.

### Kubernetes
<!-- Orchestration platform -->
Each service was deployed within the Kubernetes infrastructure locally on Minikube through the files specified in the `Kubernetes` folder. Worth mentioning is the fact that services which are stateful are implemented via `StatefulSets`.

<!-- Deployment on GCP -->
As of writing this, the application is not yet deployed on Google Cloud Platform, however we intend to make this transition before the demo.

### Frontend
<!-- What data is visualized -->
A simple webpage was built that shows

<!-- How does that gata get there -->