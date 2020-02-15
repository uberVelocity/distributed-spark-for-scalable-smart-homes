CREATE TABLE testsensorcompaction( ts timestamp, value float, primary key(server, ts) ) WITH COMPACTION = { 'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1};



CREATE KEYSPACE "household" WITH replication = {'class':'NetworkTopologyStrategy', 'replication_factor':3};

