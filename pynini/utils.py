# -*- coding: utf-8 -*-
import json
from io import StringIO
from pprint import pprint

#import yaml
import pyaml  # pip install pyaml
from jinja2 import evalcontextfilter
import mistune


#markdown = mistune.Markdown()
markdown = mistune.Markdown(escape=True, hard_wrap=True)


class SimpleLog(object):
    def __init__(self, level):
        self.level = level or 0

    def debug(self, *args):
        if self.level > 1:
            print(*args)

    def info(self, *args):
        # print("level=%s"% self.level)
        if self.level > 0:
            print(*args)

    def warn(self, *args):
        print("WARN:", *args)

    def error(self, *args):
        print("ERROR:", *args)


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


@evalcontextfilter
def count_length(eval_ctx, value):
    result = len(value)
    # if eval_ctx.autoescape:
    #    result = Markup(result)
    return str("That is %d long" % result)


def as_python(value):
    out = StringIO()
    pprint(value, out)
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