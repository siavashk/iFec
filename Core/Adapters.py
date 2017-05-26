def pad(source, symbolSize=4, paddingSymbol='X'):
    if len(source) % symbolSize == 0:
        return source, 0
    else:
        paddingSize = symbolSize - len(source) % symbolSize
        padding = paddingSymbol * paddingSize
        return source + padding, paddingSize

def unpad(source, paddingSize=4):
    if paddingSize < 0 or paddingSize >= len(source):
        raise ValueError('Negative paddingSize or padding larger than source')
    else:
        source[:-paddingSize]
