import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    data = data[data['avg_profit'] >= 5000]
    data.to_csv('gen_files_py/output6.csv', index=False)
    print('everything works!')
    return

if __name__ == '__main__':
    main()