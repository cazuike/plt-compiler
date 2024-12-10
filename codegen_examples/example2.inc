input! "testCSVs/data1.csv"
groupby! department
aggregate! sum(total_sales), avg(avg_profit)
output! "gen_files_py/output2.csv"
shout! "Grouping and aggregation completed successfully."
