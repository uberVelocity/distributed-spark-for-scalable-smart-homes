CQL="""CREATE KEYSPACE "household" WITH replication = {'class':'SimpleStrategy', 'replication_factor':3}; USE household; CREATE TABLE heatersensor(id text, model text, t float, ts timestamp, wattage float, temperature float, primary key(id, ts)) WITH COMPACTION = { 'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1}; CREATE TABLE lampsensor(id text, model text, t float, ts timestamp, wattage float, lumen float, primary key(id, ts)) WITH COMPACTION = { 'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1}; CREATE TABLE vacuumsensor(id text, model text, t float, ts timestamp, wattage float, suction float, primary key(id, ts)) WITH COMPACTION = { 'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1};"""

until echo $CQL | cqlsh; do
  echo "cqlsh: Cassandra is unavailable to initialize - will retry later"
  sleep 2
done &

exec /docker-entrypoint.sh "$@"
