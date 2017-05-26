import numpy as np
import matplotlib.pyplot as plt
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='Calculate frame loss for encoded data over a lossy channel')
    parser.add_argument('--input', dest='input', type=str)
    parser.add_argument('--output', dest='output', type=str)
    return parser.parse_args()

def main():
    args = parseArgs()
    inArray = np.load(args.input)
    p = inArray[0, :]
    e = inArray[1, :]
    plt.plot(p, e)
    plt.xlabel('Probability of packet drop')
    plt.ylabel('Probabilty of frame loss')
    plt.grid(True)
    if args.output:
        plt.savefig(args.output)
    plt.show()

if __name__ == "__main__":
    main()
