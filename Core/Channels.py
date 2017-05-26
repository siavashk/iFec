import random

def LosslessChannel(symbols):
    return symbols

def UniformLossyChannel(symbols, drop):
    results = []
    for index, symbol in enumerate(symbols):
        if (random.random() > drop):
            results.append(symbol)
    return results
