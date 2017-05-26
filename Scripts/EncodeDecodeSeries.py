import argparse
from IO import JPEGSeriesReader
from Core import pad, unpad, RaptorQEncode, RaptorQDecode
import sys

def parseArgs():
    parser = argparse.ArgumentParser(description='Display JPEG Series')
    parser.add_argument('--binary', dest='binary', type=str)
    parser.add_argument('--meta', dest='meta', type=str)
    parser.add_argument('--min', dest='minSymbolSize', type=int)
    parser.add_argument('--size', dest='symbolSize', type=int)
    parser.add_argument('--overhead', dest='overhead', type=float)
    parser.add_argument('--memory', dest='memory', type=int)
    return parser.parse_args()

def main():
    args = parseArgs()
    reader = JPEGSeriesReader(args.meta, args.binary)
    series = reader.read()
    series = [pad(elem, args.minSymbolSize)[0] for elem in series]

    sys.stdout.write(str(len(series)) + ': ')
    sys.stdout.flush()
    for index, data in enumerate(series):
        encodedData = RaptorQEncode(data, args.minSymbolSize, args.symbolSize, args.memory, args.overhead)

        # Received data
        symbols    = encodedData['symbols']
        data_len   = encodedData['data_bytes']
        oti_common = encodedData['oti_common']
        oti_scheme = encodedData['oti_scheme']

        decodedData = RaptorQDecode(symbols, data_len, oti_common, oti_scheme)
        if index % 10 == 0 and index % 100 != 0:
            if index % 100 == 0:
                sys.stdout.write('|\n')
            else:
                sys.stdout.write('|\n')
        else:
            sys.stdout.write('*')
        sys.stdout.flush()
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
