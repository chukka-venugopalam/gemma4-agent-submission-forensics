#!/usr/bin/env python3
"""Standard-library SafeTensors audit for zero-valued LoRA B matrices."""
from __future__ import annotations
import argparse, hashlib, json, struct, tempfile, zipfile
from pathlib import Path

_FORMATS = {
    'BF16': ('<H', 2, lambda x: (x & 0x7FFF) == 0),
    'F16':  ('<H', 2, lambda x: (x & 0x7FFF) == 0),
    'F32':  ('<I', 4, lambda x: (x & 0x7FFFFFFF) == 0),
    'F64':  ('<Q', 8, lambda x: (x & 0x7FFFFFFFFFFFFFFF) == 0),
    'I8':   ('<b', 1, lambda x: x == 0),
    'U8':   ('<B', 1, lambda x: x == 0),
    'I16':  ('<h', 2, lambda x: x == 0),
    'U16':  ('<H', 2, lambda x: x == 0),
    'I32':  ('<i', 4, lambda x: x == 0),
    'U32':  ('<I', 4, lambda x: x == 0),
    'I64':  ('<q', 8, lambda x: x == 0),
    'U64':  ('<Q', 8, lambda x: x == 0),
    'BOOL': ('<?', 1, lambda x: x is False),
}


def _read_safetensors(path: Path):
    raw = path.read_bytes()
    if len(raw) < 8:
        raise ValueError('file shorter than SafeTensors header prefix')
    header_len = struct.unpack('<Q', raw[:8])[0]
    if header_len > len(raw) - 8:
        raise ValueError('invalid SafeTensors header length')
    header = json.loads(raw[8:8+header_len].decode('utf-8'))
    data = raw[8+header_len:]
    results=[]
    for name, meta in header.items():
        if name == '__metadata__':
            continue
        dtype=meta['dtype']; fmt_info=_FORMATS.get(dtype)
        if fmt_info is None:
            raise ValueError(f'unsupported SafeTensors dtype: {dtype}')
        fmt, itemsize, is_zero=fmt_info
        start,end=meta['data_offsets']
        tensor_bytes=data[start:end]
        if len(tensor_bytes)%itemsize:
            raise ValueError(f'invalid byte length for tensor {name}')
        zero_count=0
        for (value,) in struct.iter_unpack(fmt,tensor_bytes):
            if is_zero(value): zero_count += 1
        total=len(tensor_bytes)//itemsize
        results.append({'name':name,'dtype':dtype,'shape':meta['shape'],'nonzero':total-zero_count,'elements':total,'all_zero':zero_count==total})
    return results


def inspect_adapter(path: Path):
    tensors=_read_safetensors(path)
    b_tensors=[x for x in tensors if 'lora_B' in x['name']]
    return {
        'file':path.name,
        'size_bytes':path.stat().st_size,
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'tensor_count':len(tensors),
        'lora_B_tensors':b_tensors,
        'all_lora_B_zero':bool(b_tensors) and all(x['all_zero'] for x in b_tensors),
        'effective_standard_lora_update_zero':bool(b_tensors) and all(x['all_zero'] for x in b_tensors),
    }


def inspect_zip(path: Path):
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(path) as z:
            names=[n for n in z.namelist() if n.startswith('adapters/') and n.endswith('adapter_model.safetensors')]
            for idx,n in enumerate(names):
                target=root/f'adapter-{idx}.safetensors'
                target.write_bytes(z.read(n))
                report=inspect_adapter(target)
                report['archive_member']=n
                yield report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('zip',type=Path,help='submission ZIP containing adapters/')
    ap.add_argument('--out',type=Path,default=Path('lora_audit.json'))
    a=ap.parse_args()
    result=list(inspect_zip(a.zip))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps({'archive':a.zip.name,'adapters':result},indent=2))
    print(a.out)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
