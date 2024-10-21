import psycopg

file="./hellolog.txt"

#DB CONFIG
DB_NAME="p1"
DB_USER="root"
DB_HOST="/var/run/postgresql"
DB_PORT="5433"
TABLE_NAME="errorlogs"

try:
    #via the psycopg library, connect to the psql database
    with psycopg.connect(
        f"dbname={DB_NAME} user={DB_USER} host={DB_HOST} port={DB_PORT}"
    ) as connection:
        #create a cursor object using psycopog's connection object
        with connection.cursor() as my_cursor:
            fatalCount = 0
            errorCount = 0
            #use the cursor object to query the database and fetch the logs
            my_cursor.execute(f"SELECT COUNT(type) FROM {TABLE_NAME} WHERE type = 'ERROR';")

            records = my_cursor.fetchall()

            for row in records:
                errorCount = row[0]

            my_cursor.execute(f"SELECT COUNT(type) FROM {TABLE_NAME} WHERE type = 'FATAL';")

            records = my_cursor.fetchall()

            for row in records:
                fatalCount = row[0]

            errorAlertFile="/root/python_revature/errorAlerts.txt"

            with open(errorAlertFile, "a") as file:

                if fatalCount >= 1 or errorCount >= 5:
                    file.write(f"Error Threshold reached with {errorCount} error(s) and {fatalCount} fatal error(s). \n")

except Exception as e:
    print("Error occured: " + e)

