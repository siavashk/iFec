from libraptorq import RQEncoder
import hashlib, base64

def RaptorQEncode(data, subsymbol_size, symbol_size, max_memory, overhead):
    data_len, data_sha256 = len(data), hashlib.sha256(data).digest()
    if data_len % 4: data += '\0' * (4 - data_len % 4)
    with RQEncoder(data, subsymbol_size, symbol_size, max_memory) as enc:
        oti_scheme, oti_common = enc.oti_scheme, enc.oti_common

        symbols, enc_k= list(), 0
        for block in enc:
            enc_k += block.symbols
            block_syms = list(block.encode_iter(repair_rate=overhead))
            symbols.extend(block_syms)

    symbols = filter(None, symbols)

    b64_encode = base64.urlsafe_b64encode

    return dict(data_bytes=data_len, oti_scheme=oti_scheme, oti_common=oti_common,
        symbols=list((s[0], b64_encode(s[1])) for s in symbols),
        checksums=dict(sha256=b64_encode(data_sha256)))
