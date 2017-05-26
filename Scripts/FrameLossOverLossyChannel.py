import argparse
from IO import JPEGSeriesReader
from Core import pad, unpad, RaptorQEncode, RaptorQDecode, UniformLossyChannel
import sys
import numpy as np

def parseArgs():
    parser = argparse.ArgumentParser(description='Calculate frame loss for encoded data over a lossy channel')
    parser.add_argument('--binary', dest='binary', type=str)
    parser.add_argument('--meta', dest='meta', type=str)
    parser.add_argument('--min', dest='minSymbolSize', type=int)
    parser.add_argument('--size', dest='symbolSize', type=int)
    parser.add_argument('--overhead', dest='overhead', type=float)
    parser.add_argument('--steps', dest='steps', type=int)
    parser.add_argument('--memory', dest='memory', type=int)
    parser.add_argument('--save', dest='save', type=str)
    return parser.parse_args()

def main():
    args = parseArgs()
    reader = JPEGSeriesReader(args.meta, args.binary)
    series = reader.read()
    series = [pad(elem, args.minSymbolSize)[0] for elem in series]

    drops  = np.linspace(0, 1, args.steps)
    errors = np.full_like(drops, 0)

    sys.stdout.write(str(len(drops)) + ':\n')
    sys.stdout.flush()
    for d, drop in enumerate(drops):
        success = 0
        fail = 0
        for data in series:
            encodedData = RaptorQEncode(data, args.minSymbolSize, args.symbolSize, args.memory, args.overhead)

            transmitted = encodedData['symbols']
            data_len    = encodedData['data_bytes']
            oti_common  = encodedData['oti_common']
            oti_scheme  = encodedData['oti_scheme']

            received = UniformLossyChannel(transmitted, drop)

            try:
                decodedData = RaptorQDecode(received, data_len, oti_common, oti_scheme)
            except:
                fail += 1
            else:
                success += 1
        errors[d] = fail / (fail + success)
        if d % 10 == 0:
            sys.stdout.write('|')
        else:
            sys.stdout.write('*')
        sys.stdout.flush()
    sys.stdout.write('\n')
    probability = np.vstack((drops, errors))
    np.save(args.save, probability)

if __name__ == "__main__":
    main()
