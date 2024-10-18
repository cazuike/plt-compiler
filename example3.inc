input! "sales.csv"
filter!  product = "Laptop"
filter! price >= 1000
groupby! region
aggregate!  sum(profit)
output! "laptop_sales.csv"