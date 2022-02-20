import sys

if __name__ == '__main__':
    DATA_ADDRESS = sys.argv[1]
    with open(DATA_ADDRESS, encoding='utf-8') as input_file:
        lines = input_file.readlines()