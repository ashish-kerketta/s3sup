import os
import unittest
import s3sup.fileprepper

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFixtureProj1(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.join(MODULE_DIR, 'fixture_proj_1')
        self.rules = s3sup.rules.load_rules(os.path.join(
            MODULE_DIR, self.project_root, 's3sup.toml'))

    def test_standard_defaults(self):
        f = s3sup.fileprepper.FilePrepper(
            self.project_root, 'products.html', self.rules)
        expected_attrs = {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'private; max-age=400'
        }
        self.assertEqual(expected_attrs, f.attributes())

    def test_image_detected(self):
        f = s3sup.fileprepper.FilePrepper(
            self.project_root, 'assets/landscape.62.png', self.rules)
        expected_attrs = {
            'Content-Type': 'image/png',
            'Cache-Control': 'max-age=12000'
        }
        self.assertEqual(expected_attrs, f.attributes())

    def test_file_content_equal_attrs_differ(self):
        f1 = s3sup.fileprepper.FilePrepper(
            self.project_root, 'about-us/index.html', self.rules)
        f1_expected_attrs = {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'private; max-age=400'
        }
        self.assertEqual(f1_expected_attrs, f1.attributes())
        f2 = s3sup.fileprepper.FilePrepper(
            self.project_root, 'about-us/duplicate.html', self.rules)
        f2_expected_attrs = {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'max-age=14000'
        }
        self.assertEqual(f2_expected_attrs, f2.attributes())
        self.assertEqual(f1.content_hash(), f2.content_hash())
        self.assertNotEqual(f1.attributes_hash(), f2.attributes_hash())