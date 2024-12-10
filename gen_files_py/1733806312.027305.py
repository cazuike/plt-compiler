import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    extra = pd.read_csv('testCSVs/data2.csv')
    data = pd.concat([data, extra], ignore_index=True)
    data.to_csv('output4.csv', index=False)
    print('Datasets combined successfully.')
    return

if __name__ == '__main__':
    main()