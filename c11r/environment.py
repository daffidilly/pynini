# -*- coding: utf-8 -*-
import configparser
import logging
import sys
from argparse import ArgumentParser
from os import getcwd, makedirs
from os.path import isdir

import arrow as arrow
import jinja2
from pathlib import Path

from jinja2 import ChoiceLoader

from .processing import JinjaProcessor, DefaultProcessor
from .data import DataLoader
from .exceptions import SetupError
from .utils import auto_str, as_python, as_json, as_yaml, filter_markdown_to_html

logger = logging.getLogger(__name__)
sect = 'conflatinator'


def check_dirs(kind, dir_or_dirs, create=False):
    if not dir_or_dirs:  # None or anything falsy
        return dir_or_dirs
    elif isinstance(dir_or_dirs, str):
        dirs = [dir_or_dirs]
    else:
        dirs = dir_or_dirs

    for d in dirs:
        if not isdir(d):
            if create:
                makedirs(d)
            else:
                raise SetupError("{} directory '{}' not found".format(kind, d))
    return dir_or_dirs


@auto_str
class Environment(object):
    def __init__(self,
                 operation_dir,
                 paths,
                 src_dir,
                 output_dir,
                 include_dirs,
                 verbosity=0,
                 data_loaders=None,
                 # template_extensions=None,
                 template_loader=None,
                 template_writer=None):
        self.paths = paths
        self.operation_dir = operation_dir
        self.src_dir = src_dir
        self.output_dir = output_dir
        self.include_dirs = include_dirs
        # self.data_extensions = self.data_loaders.keys()
        # self.template_extensions = template_extensions or ('.jinja2',)
        jinja_processor = JinjaProcessor()
        self.processors = {
            '.jinja2': jinja_processor,
            '.jinja': jinja_processor,
            '.j2': jinja_processor,
        }
        self.default_processor = DefaultProcessor()

        self.verbosity = verbosity

        self.mkdir_perms = 0o777  # TODO: is this needed?

        # find templates in both the src dir and the list of include dirs
        template_loader = template_loader or jinja2.FileSystemLoader(
            [self.src_dir] + self.include_dirs, )

        # self.template_writer = template_writer or TemplateFileWriter()

        data_loader = DataLoader()
        # see http://jinja.pocoo.org/docs/dev/api/#high-level-api
        self.jinja = jinja2.Environment(
            loader=ChoiceLoader([data_loader, template_loader]),
            trim_blocks=True,
            lstrip_blocks=True,
            # extensions=(DataLoaderExtension,),
            # extensions=('c11r.data.DataLoaderExtension',),
        )

        self.jinja.filters['as_python'] = as_python
        self.jinja.filters['as_json'] = as_json
        self.jinja.filters['as_yaml'] = as_yaml
        self.jinja.filters['as_markdown'] = filter_markdown_to_html

        self.global_vars = dict(
            when=arrow.utcnow()
        )

    def processor_for_ext(self, ext):
        return self.processors.get(ext, self.default_processor)


def auto_config(operation_dir=None):
    operation_dir = operation_dir or getcwd()
    config = configparser.ConfigParser()
    config[sect] = {
        'src_dir': 'web',
        'output_dir': 'dist',  # or release or output?
        'include_dirs': '',
        'verbosity': '0',
    }

    # import pdb; pdb.set_trace()
    ini_file_dir = Path(operation_dir)
    names = [
        ini_file_dir / 'c11r.ini',
        ini_file_dir / 'conflatinator.ini',
    ]
    logger.debug('ini candidate names: %s', names)
    loaded_files = config.read(names)
    logger.debug('loaded_files: %s', loaded_files)

    logger.debug('config: %s', {section: dict(config[section]) for section in config.sections()})
    return config


def auto(argv=None, prog=None):
    argv = argv or sys.argv  # use command-line flags if nothing else passed
    if not prog:
        prog = Path(argv[0]).name

    operation_dir = getcwd()
    config = auto_config(operation_dir)

    arg_parser = ArgumentParser(prog=prog, description='Static HTML generator')
    arg_parser.add_argument('paths', metavar='path', type=str, nargs='*',
                            help='paths to load')
    arg_parser.add_argument('--verbosity', '-v',
                            action='count',
                            help='increase log verbosity',
                            default=config.get(sect, 'verbosity'))
    arg_parser.add_argument('--src', '-s',
                            metavar='dir',
                            help='directory to read src files from',
                            default=config.get(sect, 'src_dir'))
    arg_parser.add_argument('--output', '-o',
                            metavar='dir',
                            help='directory to write output to',
                            default=config.get(sect, 'output_dir'))
    arg_parser.add_argument('--include', '-i',
                            action='append',
                            metavar='dir',
                            help='add this directory to include path (specify as many times as needed)',
                            default=config.get(sect, 'include_dirs', fallback='').split())

    parsed_args = arg_parser.parse_args(argv[1:])
    logger.debug('parsed: %s', parsed_args)
    logger.debug('paths: %s', parsed_args.paths)
    logger.debug('src_dir: %s', parsed_args.src)
    logger.debug('output_dir: %s', parsed_args.output)
    logger.debug('include_dirs: %s', parsed_args.include)

    if not parsed_args.include:
        # Default to include the 'templates' dir ... is this too magic?
        # if isdir('templates'):
        #     parsed_args.include = ['templates']
        # elif isdir('layouts'):
        #     parsed_args.include = ['layouts']
        parsed_args.include = ['.']

    src_dir = check_dirs('src', parsed_args.src)
    output_dir = check_dirs('output', parsed_args.output, create=True)
    include_dirs = check_dirs('include', parsed_args.include)

    return Environment(operation_dir,
                       paths=parsed_args.paths or [src_dir],
                       src_dir=src_dir,
                       output_dir=output_dir,
                       include_dirs=include_dirs,
                       verbosity=parsed_args.verbosity,
                       template_loader=None,
                       template_writer=None)
