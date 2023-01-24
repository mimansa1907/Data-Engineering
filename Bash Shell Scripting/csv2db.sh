# This script
# Extracts data from /etc/passwd/ file into CSV file.

# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd

# Transforms the text delimiter from ':' to ','.
# Loads the data from the CSV file into a table in 
# PostgreSQl database.

echo "Extracting Data"

# Extract the columns 1(user name), 2(user id) and 
# 6 (home directory path) from /etc/passwd

cut -d":" -f1,3,6 /etc/passwd > extracted_data.txt

echo "Printing Extracted Data"
cat extracted_data.txt

echo "Tranforming data"
tr ":" "," < extracted_data.txt > transformed_data.csv

echo "Printing Transformed data"
cat transformed_data.csv

echo "Loading data"
# Load phase
echo "Loading data"
# Send the instructions to connect to 'template1' and
# copy the file to the table 'users' through command pipeline.

echo "\c template1;\COPY users  FROM '/home/project/transformed_data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=localhost
