import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    data = data[data['avg_profit'] >= 5000]
    data = data.sort_values(by=['total_sales'], ascending=[False])
    data.to_csv('gen_files_py/output3.csv', index=False)
    print('Filtering and sorting completed successfully.')
    return

if __name__ == '__main__':
    main()