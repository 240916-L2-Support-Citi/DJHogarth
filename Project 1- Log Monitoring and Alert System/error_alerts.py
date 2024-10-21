import psycopg

file="./hellolog.txt"

#DB CONFIG
DB_NAME="p1"
DB_USER="root"
DB_HOST="/var/run/postgresql"
DB_PORT="5433"
TABLE_NAME="errorlogs"

try:
    # via the psycopg library, connect to the psql database
    with psycopg.connect(
        f"dbname={DB_NAME} user={DB_USER} host={DB_HOST} port={DB_PORT}"
    ) as connection:
        # create a cursor object using psycopog's connection object
        with connection.cursor() as my_cursor:
            fatalCount = 0
            errorCount = 0
            # use the cursor object to query the database and fetch the logs
            my_cursor.execute(f"SELECT COUNT(type) FROM {TABLE_NAME} WHERE type = 'ERROR';")

            records = my_cursor.fetchall()
            # store number of logs of type ERROR from the query in the errorCount variable
            for row in records:
                errorCount = row[0]

            my_cursor.execute(f"SELECT COUNT(type) FROM {TABLE_NAME} WHERE type = 'FATAL';")

            records = my_cursor.fetchall()

            # store the number of logs of type FATAL from the query in the fatalCount variable
            for row in records:
                fatalCount = row[0]

            #Define the path to the file that stores the error threshold alerts
            errorAlertFile="/root/python_revature/errorAlerts.txt"

            # Append the threshold alerts to the file if the threshold of 1 fatal and 5 errors have been reached
            with open(errorAlertFile, "a") as file:

                if fatalCount >= 1 or errorCount >= 5:
                    file.write(f"Error Threshold reached with {errorCount} error(s) and {fatalCount} fatal error(s). \n")

except Exception as e:
    print("Error occured: " + e)

