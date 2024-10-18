input! "employeeee_data.csv"
groupby! department
aggregate! avg(salary)
output! "avg_salaries.csv"