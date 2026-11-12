import csv, sys, tempfile, unittest, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import afsa

class AFSATests(unittest.TestCase):
    def make_zip(self, path, files, date=(2026,1,1,0,0,0)):
        with zipfile.ZipFile(path,'w') as z:
            for name, data in files.items():
                info=zipfile.ZipInfo(name, date_time=date)
                z.writestr(info, data)

    def test_same_payload_different_zip_timestamp(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/'a.zip',Path(d)/'b.zip'
            fs={'agent.yaml':'model: x\n','prompts/system.md':'hello'}
            self.make_zip(a,fs,(2026,1,1,0,0,0)); self.make_zip(b,fs,(2026,2,2,0,0,0))
            self.assertNotEqual(afsa.sha256_bytes(a.read_bytes()),afsa.sha256_bytes(b.read_bytes()))
            self.assertEqual(afsa.canonical_payload(a)[0],afsa.canonical_payload(b)[0])

    def test_payload_changes_when_file_bytes_change(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/'a.zip',Path(d)/'b.zip'
            self.make_zip(a,{'agent.yaml':'model: x'})
            self.make_zip(b,{'agent.yaml':'model: y'})
            self.assertNotEqual(afsa.canonical_payload(a)[0],afsa.canonical_payload(b)[0])

    def test_member_path_is_part_of_fingerprint(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/'a.zip',Path(d)/'b.zip'
            self.make_zip(a,{'a.txt':'same'}); self.make_zip(b,{'b.txt':'same'})
            self.assertNotEqual(afsa.canonical_payload(a)[0],afsa.canonical_payload(b)[0])

    def test_score_mapping_known_values(self):
        self.assertEqual(afsa.solve_bounds(.20,58),(12,12))
        self.assertEqual(afsa.solve_bounds(.15,58),(9,9))
        self.assertEqual(afsa.solve_bounds(.12,58),(7,7))

    def test_missing_archive_fails_loudly(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manifest=root/'m.csv'; manifest.write_text('archive,score\nmissing.zip,0.20\n')
            with self.assertRaises(FileNotFoundError): afsa.audit_manifest(manifest,root,root/'out',58)

    def test_malformed_zip_fails_loudly(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.zip'; p.write_bytes(b'not a zip')
            with self.assertRaises(zipfile.BadZipFile): afsa.canonical_payload(p)

if __name__ == '__main__': unittest.main()
