input! "log_data.csv"
filter! event_type = "ERROR"
shout!  "Critical errors found in logs"
output!  "error_logs.csv"