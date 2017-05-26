from libraptorq import RQDecoder, RQError
import base64

def RaptorQDecode(symbols, data_len, oti_common, oti_scheme):
    b64_decode = lambda s:\
        base64.urlsafe_b64decode(bytes(s))\
            if '-' in s or '_' in s else bytes(s).decode('base64')

    with RQDecoder(oti_common, oti_scheme) as dec:
        for sym_id, sym in symbols:
            sym_id, sym = int(sym_id), b64_decode(sym)
            try:
                dec.add_symbol(sym, sym_id)
            except RQError as err:
                continue
        return dec.decode()[:data_len]
