#    Copyright (C) 2011 - 2014  Canonical Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import argparse
import json
import sys
from fnmatch import fnmatch
from subprocess import check_output, CalledProcessError

import yaml


class Description(argparse._StoreTrueAction):
    """A argparse action that prints parent parser's description & exits."""
    def __call__(self, parser, namespace, values, option_string=None):
        print(parser.description.split('\n')[0].strip('. '))
        raise SystemExit()


class Config:
    def __init__(self, args=None):
        for name, value in vars(self._parse_args(args)).items():
            setattr(self, name, value)
        self._formatter = getattr(self, '_{}_formatter'.format(self.format))

    def _parse_args(self, args):
        parser = argparse.ArgumentParser(
            description='show details about config for a charm from the store')
        parser.add_argument('charm', help='charm ID')
        parser.add_argument('-c', '--channel',
                            choices=['stable', 'candidate', 'beta',
                                     'edge', 'unpublished'],
                            help='the channel of the charm or bundle to use')
        parser.add_argument('option_names', nargs='*',
                            help='name of option(s) to include')
        parser.add_argument('-a', '--agent', nargs=1,
                            help='name of file containing agent login details')
        parser.add_argument('--auth',
                            help='user:passwd to use for basic HTTP '
                                 'authentication')
        parser.add_argument('-f', '--format', default='tabular',
                            choices=['tabular', 'yaml', 'json', 'value'],
                            help='format for output')
        parser.add_argument('--description', action=Description)
        return parser.parse_args(args)

    def _filter(self, data):
        if self.option_names:
            return {opt: info for opt, info in data.items()
                    if any(fnmatch(opt, pat) for pat in self.option_names)}
        else:
            return data

    def _load(self):
        cmd = ['charm', 'show', '--format=yaml', self.charm, 'charm-config']
        if self.channel:
            cmd.extend(['--channel', self.channel])
        if self.auth:
            cmd.extend(['--auth', self.auth])
        try:
            stdout = check_output(cmd)
        except CalledProcessError as e:
            sys.exit(e.returncode)
        return yaml.safe_load(stdout).get('charm-config', {}).get('Options')

    def _yaml_formatter(self, data):
        return yaml.dump(data, default_flow_style=False).splitlines()

    def _json_formatter(self, data):
        return json.dumps(data, sort_keys=True, indent=2).splitlines()

    def _value_formatter(self, data):
        opts = self.option_names or sorted(data.keys())
        return [str(data[opt]['Default']) for opt in opts]

    def _tabular_formatter(self, data):
        try:
            from shutil import get_terminal_size
            width = get_terminal_size(fallback=(120, 0))[0]
        except ImportError:
            width = 120
        opt_width = max(len(opt) for opt in data.keys())
        val_width = min(max(len(repr(opt['Default']))
                            for opt in data.values()), 30)
        max_dsc_width = width - opt_width - val_width - 13
        dsc_width = min(max(len(opt['Description'].strip())
                            for opt in data.values()), max_dsc_width)
        fmt = '{{:{}}}  {{:{}}}  {{:7}}  {{:{}}}'.format(opt_width,
                                                         val_width,
                                                         dsc_width)
        headers = fmt.format('Option', 'Value', 'Type', 'Description').strip()
        lines = [headers, '-' * len(headers)]
        for opt, info in sorted(data.items()):
            value = repr(info['Default'])
            if len(value) > 30:
                if info['Type'] == 'string':
                    value = value[:26] + "'..."
                else:
                    value = value[:27] + '...'
            desc = info['Description'].replace('\n', ' ').strip()
            if len(desc) > max_dsc_width:
                desc = desc[:max_dsc_width-3] + '...'
            lines.append(fmt.format(
                opt,
                value,
                info['Type'],
                desc,
            ).strip())
        return lines

    def _output(self, text, stderr=False):
        print(text, file=sys.stderr if stderr else sys.stdout)

    def _main(self):
        data = self._filter(self._load())
        if data:
            self._output('\n'.join(self._formatter(data)))
        else:
            self._output('No options found.', stderr=True)
            sys.exit(1)

    @classmethod
    def main(cls):
        cls()._main()


if __name__ == '__main__':
    Config.main()
