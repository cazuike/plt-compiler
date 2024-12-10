import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    data = data.groupby('department')
    data = data.agg({'total_sales': 'sum', 'avg_profit': 'mean'}).reset_index()
    data = data.rename(columns={'total_sales': 'total_total_sales', 'avg_profit': 'avg_avg_profit'})
    data.to_csv('gen_files_py/output2.csv', index=False)
    print('Grouping and aggregation completed successfully.')
    return

if __name__ == '__main__':
    main()