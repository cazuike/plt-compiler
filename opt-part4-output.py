import pandas as pd

def main():
    data = pd.read_csv('testCSVs/data1.csv')
    numeric = data.select_dtypes(include=['number']).columns
    data[numeric] = data[numeric] * 6
    numeric = data.select_dtypes(include=['number']).columns
    data[numeric] = data[numeric] * 2
    data = data.sort_values(by=['name'], ascending=[False])
    print('keep this line')
    data.to_csv('p4_output.csv', index=False)
    return

if __name__ == '__main__':
    main()