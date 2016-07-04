# -*- coding: utf-8 -*-
import sys
import errno
import os
import json
import pyaml
import mistune

from jinja2 import evalcontextfilter
from pprint import pprint

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3


markdown = mistune.Markdown(escape=True, hard_wrap=True)


def mkdir_p_polyfill(path, perms, exist_ok):
    """Make directories including parents.
    Python >= 3.2 doesn't need this because the exist_ok parameter is there.
    However, earlier python versions don't have that.
    See http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python/600612#600612
    """
    try:
        os.makedirs(path, perms)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


mkdir_p = mkdir_p_polyfill if sys.version_info < (3, 2) else os.makedirs


class SimpleLog(object):
    def __init__(self, level):
        self.level = level or 0

    def debug(self, *args):
        if self.level > 1:
            print(' '.join(args))

    def info(self, *args):
        # print("level=%s"% self.level)
        if self.level > 0:
            print(' '.join(args))

    def warn(self, *args):
        print("WARN:", ' '.join(args))

    def error(self, *args):
        print("ERROR:", ' '.join(args))


def auto_str(cls):
    """Decorator that adds a default __str__ to a class.

    see http://stackoverflow.com/a/33800620/963195
    """

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


# TODO DELETE
@evalcontextfilter
def count_length(eval_ctx, value):
    result = len(value)
    # if eval_ctx.autoescape:
    #    result = Markup(result)
    return str("That is %d long" % result)


def as_python(value):
    out = StringIO()
    ##pprint(value, out)
    return out.getvalue()


def as_json(value):
    return json.dumps(value, indent=2, sort_keys=True)


def as_yaml(value):
    #return yaml.dump(value, indent=2, line_break='\n')
    return pyaml.dump(value)#, indent=2, line_break='\n')


@evalcontextfilter
def filter_markdown_to_html(eval_ctx, value):
    # if eval_ctx.autoescape:
    #    result = Markup(result)
    return markdown(value)