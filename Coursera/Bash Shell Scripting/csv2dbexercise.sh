echo "Extacting Data"
cut -d"#" -f1-4 web-server-access-log.txt  > extracted-data.txt

echo "Transforming data"
tr "#" "," < extracted-data.txt > transformed-data.csv


echo "Loading data"
echo "\c template1;\COPY access_log  FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=localhost

