input! "testCSVs/data1.csv"
filter! avg_profit >= 5000
sort! total_sales desc
output! "gen_files_py/output3.csv"
shout! "Filtering and sorting completed successfully."
