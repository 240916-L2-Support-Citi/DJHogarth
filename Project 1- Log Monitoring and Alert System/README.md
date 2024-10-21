# Log Monitoring and Alert System

This project simulates a real-world production support tool that monitors log files for errors and generates alerts when specific thresholds are exceeded. The system consists of three primary components:

1. **Log Generation**: A Bash script (`generate_logs.sh`) simulates application logs with varying severity levels such as `INFO`, `WARNING`, `ERROR`, and `FATAL`.
2. **Log Monitoring and Storage**: Another Bash script (`log_monitor.sh`) monitors the generated logs, filters for `ERROR` and `FATAL` entries, and stores them in a PostgreSQL database.
3. **Alert System**: A Python script (`error_alerts.py`) queries the PostgreSQL database and triggers alerts when the number of `ERROR` logs exceeds 5 or `FATAL` logs exceeds 1.

## Features
- Log generation and real-time monitoring using Bash scripts.
- PostgreSQL database integration for log storage and tracking.
- Python-based alert system for threshold monitoring.
- Cron job automation for continuous log monitoring and alerting.

---

## How to Run the Project

### Step 1: Set Up PostgreSQL Database
Install PostgreSQL:
   ```bash
   sudo -u postgres psql
   ```
Install psychopg on your unix based system:
 ```bash
   sudo apt install python3-psycopg
   ```

### Step 2: Change File Permissions for generate_logs.sh and Run the Script
Change the permissions of the script so it can be executed and then run it:
```bash
chmod +x generate_logs.sh
./generate_logs.sh
```
This script is responsible for generating the logs of varying types. After runnning the script, 
you may want to want a minute or two so the file can generate a decent amount of logs. 

### Step 3: Add Cron Jobs for log.monitor.sh and error_alerts.py.
:
```bash
crontab -e
```
Add cron jobs to run the files every minute:
```bash
* * * * * /{your_own_path}/log_monitor.sh
* * * * * /usr/bin/python3 /{your_own_path}/error_alerts.py
```
This script monitors the log file and stores `ERROR` and `FATAL` logs in the PostgreSQL database.
Replace "your_own_path" with the absolute path of your file. You can use the pwd command (if on unix based system) to see the absolute path of the file.

### Step 4: Check the Database to View Filtered Logs
Use the psql command to access the posgresql "p1" database which was created within the log.monitor script.
Then query the database to display the records in the table. This table only has three columns: 
time (time stamp of log), type (log level), message (a brief description of the error).
```bash
psql p1
SELECT * FROM errorlogs; 
```
You should now see the error and fatal logs within the table. New logs will be added every minute due to how the cron jobs
were setup. 
---