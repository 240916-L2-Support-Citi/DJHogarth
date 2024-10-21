#!/bin/bash

#DB CONFIG
DB_NAME="p1"
DB_USER="root"
DB_HOST="/var/run/postgresql"
DB_PORT="5433"
TABLE_NAME="errorlogs"

#DB CONST QUERIES

#SQL query for creating the database if none already exists
CREATE_NEW_DB="SELECT 'CREATE DATABASE test' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test')\gexec;"
# SQL query for creating posgresql table for storing all the error and fatal error logs
CREATE_NEW_TABLE="CREATE TABLE IF NOT EXISTS $TABLE_NAME (error_id SERIAL PRIMARY KEY, time TIMESTAMP NOT NULL, type VARCHAR (50) NOT NULL, message VARCHAR (255));"

#Create the database if none exists
psql -U "$DB_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 | psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME"

#Create Errorlogs table if none exists
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$CREATE_NEW_TABLE"

#filter the log file for only logs that FATAL or ERROR, and not contain (rd), indicating the line hasn't been read yet
buffer=$(grep -E 'FATAL|ERROR' /var/log/app.log | grep -v ' (rd) ')

#add (rd) to the beginning of each line of the file containing the generated logs, to indicate each log has already been read
sed -i -E '/ERROR|FATAL/{ /\(rd\)/!s/^/ (rd) /; }' /var/log/app.log

#Loop through each line in the buffer, and extract out the timestamps, error type and error message of each line

while ISF= read -r line; do

    time_stamp=$(echo "$line" | grep -oP "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    error_type=$(echo "$line" | grep -oP "FATAL|ERROR")
    error_text=$(echo "$line" | grep -oP "(?<=\[(FATAL|ERROR)\] ).*$")

    #SQL INSERT query for adding the log into the SQL table, errorlogs 
    INSERT="INSERT INTO errorlogs(time, type, message) VALUES ('$time_stamp', '$error_type', '$error_text');"

    #Execute insert query
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$INSERT" 

done <<< "$buffer"
