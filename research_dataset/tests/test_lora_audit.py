import json, struct, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lora_audit

class LoRAAuditTests(unittest.TestCase):
    def write_safe(self, path):
        # Tiny SafeTensors: A has two nonzero BF16 values; B is all-zero.
        header={
            'layer.q_proj.lora_A.weight': {'dtype':'BF16','shape':[1,2],'data_offsets':[0,4]},
            'layer.q_proj.lora_B.weight': {'dtype':'BF16','shape':[2,1],'data_offsets':[4,8]},
        }
        h=json.dumps(header,separators=(',',':')).encode()
        payload=struct.pack('<HHHH',0x3f80,0x4000,0,0)
        path.write_bytes(struct.pack('<Q',len(h))+h+payload)

    def test_zero_B_detected_and_A_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'adapter.safetensors'; self.write_safe(p)
            tensors=lora_audit._read_safetensors(p)
            a=next(x for x in tensors if 'lora_A' in x['name'])
            b=next(x for x in tensors if 'lora_B' in x['name'])
            self.assertEqual(a['nonzero'],2)
            self.assertTrue(b['all_zero'])

    def test_invalid_header_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.safetensors'; p.write_bytes(b'bad')
            with self.assertRaises(ValueError): lora_audit._read_safetensors(p)

if __name__=='__main__': unittest.main()
