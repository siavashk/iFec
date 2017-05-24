import json

class JPEGSeriesReader(object):
    def __init__(self, meta, binary):
        self.meta   = meta
        self.binary = binary
        self.separator = ""

    @staticmethod
    def readMeta(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def readBinary(filename):
        with open(filename, 'rb') as f:
            return f.read()

    def printSelf(self):
        print self.readMeta(self.meta)
        print self.readBinary(self.binary)

    def read(self):
        meta = self.readMeta(self.meta)
        self.separator = "---" + meta["id"] + "---"
        byte = self.readBinary(self.binary)
        series = byte.encode('hex').split(self.separator.encode('hex'))
        return [elem.decode('hex') for elem in series]
