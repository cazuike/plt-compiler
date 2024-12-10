import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    data = data.rename(columns={'total_sales': 'revenue'})
    numeric = data.select_dtypes(include=['number']).columns
    data[numeric] = data[numeric] * 2
    data.to_csv('output5.csv', index=False)
    print('Renaming and multiplication completed successfully.')
    return

if __name__ == '__main__':
    main()