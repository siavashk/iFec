import argparse
from IO import JPEGSeriesReader
import io
from PIL import Image

def parseArgs():
    parser = argparse.ArgumentParser(description='Display a series of jpeg images')
    parser.add_argument('--binary', dest='binary', type=str)
    parser.add_argument('--meta', dest='meta', type=str)
    return parser.parse_args()

def main():
    args = parseArgs()
    reader = JPEGSeriesReader(args.meta, args.binary)
    series = reader.read()
    for elem in series:
        image = Image.open(io.BytesIO(elem))
        image.show()

if __name__ == "__main__":
    main()
