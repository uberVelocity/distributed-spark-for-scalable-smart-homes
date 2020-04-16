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

<!-- Advantages of using said database -->

<!-- Replicability strategy -->

<!-- Compaction -->

<!-- Interface of Database -->

<!-- What do you store in it (what tables, historical data) -->

<!-- Initialization of database -->

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

<!-- Volumes used for Cassandra, Kafka, and Zookeeper -->

### Kubernetes
<!-- Orchestration platform -->

<!-- Deployment on Minikube -->

<!-- Deployment on GCP -->

### Frontend
<!-- What data is visualized -->

<!-- How does that gata get there -->