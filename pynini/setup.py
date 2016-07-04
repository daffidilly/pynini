# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser
from os import getcwd
from os.path import dirname, basename, join, isdir

import jinja2

from pynini.data import YamlDataLoader
from pynini.exceptions import SetupError
from pynini.utils import auto_str, count_length, as_python, as_json, as_yaml, filter_markdown_to_html, SimpleLog
from pynini.writing import TemplateFileWriter


@auto_str
class Setup(object):
    def __init__(self, operation_dir, dist_dir, src_dir,
                 pages_dir=None, layouts_dir=None, partials_dir=None,
                 verbosity=0,
                 template_loader=None,
                 template_writer=None):
        self.operation_dir = operation_dir
        self.dist_dir = dist_dir
        self.src_dir = src_dir
        self.pages_dir = pages_dir or join(src_dir, 'pages')
        self.layouts_dir = layouts_dir or join(src_dir, 'layouts')
        self.partials_dir = partials_dir or join(src_dir, 'partials')
        self.data_loaders = {
            YamlDataLoader.extension: YamlDataLoader(),
        }
        self.data_extensions = self.data_loaders.keys()
        self.template_extensions = ('.html',)

        self.verbosity = verbosity
        self.log = SimpleLog(level=self.verbosity)

        self.mkdir_perms = 0o777

        template_loader = template_loader or jinja2.FileSystemLoader([
            self.src_dir, self.layouts_dir, self.pages_dir, self.partials_dir],
        )

        self.template_writer = template_writer or TemplateFileWriter()

        # see http://jinja.pocoo.org/docs/dev/api/#high-level-api
        self.jinja = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        self.jinja.filters['count_length'] = count_length
        self.jinja.filters['as_python'] = as_python
        self.jinja.filters['as_json'] = as_json
        self.jinja.filters['as_yaml'] = as_yaml
        self.jinja.filters['as_markdown'] = filter_markdown_to_html

        # self.jinja.filters['count_length'] = count_length
        # self.jinja.filters['count_length'] = count_length
        ##print(self.jinja.filters)


    @staticmethod
    def determine(argv=None):
        argv = argv or sys.argv  # use command-line flags if nothing else passed

        arg_parser = ArgumentParser(prog='pynini', description='Static site processor')
        arg_parser.add_argument('--verbosity', '-v', action='count', help='increase log verbosity', default=0)
        arg_parser.add_argument('--dist', metavar='dist_dir', help='specify dist directory (disable auto detect)', default=None)
        arg_parser.add_argument('--src', '-s', metavar='src_dir', help='specify src directory (disable auto detect)', default=None)
        arg_parser.add_argument('--pages', metavar='pages_dir', help='specify pages directory (disable auto detect)', default=None)
        arg_parser.add_argument('--layouts', metavar='layouts_dir', help='specify layouts directory (disable auto detect)', default=None)
        arg_parser.add_argument('--partials', metavar='partials_dir', help='specify partials directory (disable auto detect)', default=None)
        parsed_args = arg_parser.parse_args(argv[1:])
        # print(parsed_args)

        # each of the below can be None
        dist_dir = parsed_args.dist
        src_dir = parsed_args.src
        pages_dir = parsed_args.pages
        layouts_dir = parsed_args.layouts
        partials_dir = parsed_args.partials

        operation_dir = getcwd()
        if isdir(join(operation_dir, 'src')):
            src_dir = src_dir or join(operation_dir, 'src')
            dist_dir = dist_dir or join(operation_dir, 'dist')

        elif 'src' == basename(operation_dir):  # we're inside the src dir
            src_dir = src_dir or operation_dir
            dist_dir = dist_dir or join(dirname(operation_dir), 'dist')

        elif not src_dir or not dist_dir:
            raise SetupError('Could not determine src_dir, dist_dir')

        return Setup(operation_dir,
                     dist_dir,
                     src_dir,
                     pages_dir=pages_dir,
                     layouts_dir=layouts_dir,
                     partials_dir=partials_dir,
                     verbosity=parsed_args.verbosity,
                     template_loader=None,
                     template_writer=None)
