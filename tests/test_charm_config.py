from unittest import TestCase
from mock import patch

import yaml
from charm_config import Config


class ConfigTest(TestCase):
    def setUp(self):
        p = patch('charm_config.check_output')
        self.mock_check_output = p.start()
        self.addCleanup(p.stop)
        self.charm_config = {
            'foo': {
                'Default': True,
                'Description': 'Does the foo if true\n'
                               'or the bar if false\n',
                'Type': 'boolean',
            },
            'qux-url': {
                'Default': 'https://qux.io/with-a-long-url',
                'Description': 'URL to find the qux',
                'Type': 'string',
            },
        }
        self.mock_check_output.side_effect = lambda *a, **kw: yaml.dump({
            'charm-config': {'Options': self.charm_config},
        })

    def test_main(self):
        config = Config(['cs:dummy-charm', '-f=value'])
        config._filter = lambda d: {}

    def test_load(self):
        config = Config(['cs:dummy-charm', '--channel', 'edge', '--auth=foo'])
        self.assertEqual(config._load(), self.charm_config)
        self.assertEqual(self.mock_check_output.call_args[0][0], [
            'charm', 'show', '--format=yaml', 'cs:dummy-charm', 'charm-config',
            '--channel', 'edge', '--auth', 'foo',
        ])

    def test_load_none(self):
        self.charm_config = {}
        config = Config(['cs:dummy-charm'])
        self.assertEqual(config._load(), {})
        self.assertEqual(self.mock_check_output.call_args[0][0], [
            'charm', 'show', '--format=yaml', 'cs:dummy-charm', 'charm-config',
        ])

    def test_filter(self):
        config = Config(['cs:dummy-charm', 'foo', 'bar'])
        results = config._filter(self.charm_config)
        assert results == {'foo': self.charm_config['foo']}

    def test_filter_glob(self):
        config = Config(['cs:dummy-charm', '*o*'])
        results = config._filter(self.charm_config)
        assert results == {'foo': self.charm_config['foo']}

    def test_filter_missing(self):
        config = Config(['cs:dummy-charm', 'bar'])
        results = config._filter(self.charm_config)
        assert results == {}

    def test_value_formatter(self):
        config = Config(['cs:dummy-charm'])
        result = config._value_formatter(self.charm_config)
        self.assertEqual(result, ["True", "https://qux.io/with-a-long-url"])

    def test_tabular_formatter(self):
        config = Config(['cs:dummy-charm'])
        with patch('shutil.get_terminal_size', create=True,
                   return_value=(64, 0)):
            actual = config._tabular_formatter(self.charm_config)
        expected = (
            "Option   Value                           Type     Description",
            "-------------------------------------------------------------",
            "foo      True                            boolean  Does the fo...",
            "qux-url  'https://qux.io/with-a-lon'...  string   URL to find...",
        )
        for i in range(len(expected)):
            self.assertEqual(actual[i], expected[i])
