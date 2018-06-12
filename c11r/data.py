import io
import json
import logging
from configparser import ConfigParser

from os.path import isfile, splitext

import yaml
import jinja2.ext
from jinja2 import TemplateNotFound

from c11r.exceptions import SetupError

logger = logging.getLogger(__name__)


def yaml_to_template(filename):
    """Load the given YAML filename, and generate a Jinja template
    that sets variable(s) to represent that data.

    This is... not the most ideal solution.

    A more ideal solution would generate Jinja2 nodes representing
    the data, rather than load YAML then generate text then parse the
    text. Still, this is a pragmatic solution.
    """
    with open(filename) as f:
        data = yaml.load(f)

    out = io.StringIO()
    out.write('{# loaded YAML from %r #}\n' % filename)
    for k, v in data.items():
        out.write('{{% set {}={} %}}\n'.format(k, repr(v)))
    return out.getvalue()


def json_to_template(filename):
    with open(filename) as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise SetupError("JSON file {} does not contain an object (dict) as the sole root object".format(filename))

    logger.info("%s -> %s", filename, data)
    out = io.StringIO()
    out.write('{# loaded JSON from %r #}\n' % filename)
    for k, v in data.items():
       out.write('{{% set {}={} %}}\n'.format(k, repr(v)))
    # out.write('{{% set {}={} %}}\n'.format('json', repr(data)))
    logger.debug("  %s -> >>>%s<<<", filename, out.getvalue())
    return out.getvalue()


def ini_to_template(filename):
    cfg = ConfigParser()
    cfg.read(filename)
    out = io.StringIO()
    out.write('{# loaded INI data from %r #}\n' % filename)
    for section in cfg.sections():
        key = section  # TODO: clean name, e.g. remove spaces, '-', etc.
        value = dict(cfg.items(section))
        out.write('{{% set {}={} %}}\n'.format(key, value))
    return out.getvalue()


data_formats = {
    '.yml': yaml_to_template,
    '.yaml': yaml_to_template,
    '.json': json_to_template,
    '.ini': ini_to_template,
}


class DataLoader(jinja2.loaders.BaseLoader):
    """Loader that converts YAML and JSON files into Jinja2 templates.
    Use in a template like this:

        {% import 'data/main.yml' as data %}

    Configure like this:

        jinja = jinja2.Environment(
            loader=ChoiceLoader([
                DataLoader(),
                jinja2.FileSystemLoader(list_of_dirs_here),
            ...
            ])

    Using `ChoiceLoader` means that the DataLoader will be attempted first,
    but will fail to match non `.yml` and `.json` files, letting other
    loaders continue.

    Writing a dedicated extension is an alternative approach that may
    have benefits, but this approach means "import ..." works.
    """
    def get_source(self, environment, template):
        # logger.info("DataLoader %s %s", environment, template)
        _, ext = splitext(template)
        data_loader = data_formats.get(ext.lower())
        if data_loader:
            if not isfile(template):
                raise TemplateNotFound(template)

            contents = data_loader(template)
            # logger.debug("loaded %s -> %s", template, contents)
            return contents, template, True

        raise TemplateNotFound(template)


# class DataLoaderExtension(jinja2.ext.Extension):
#     r""" Adds a {% data %} tag to Jinja.
#
#     See: https://stackoverflow.com/questions/1521909/how-create-jinja2-extension
#     """
#
#     tags = {'data', 'data_load', 'load'}
#     # template = u'<input type="hidden" name="csrfmiddlewaretoken" value="%s">'
#
#     def parse(self, parser):
#         logger.debug('here %s', parser)
#         lineno = next(parser.stream).lineno
#         ctx_ref = jinja2.nodes.ContextReference()
#
#         # Parse a single expression that is the 'bundle' or 'config:bundle'
#         args = [ctx_ref, parser.parse_expression()]
#
#         # name = parser.stream.expect('string')
#         # logger.debug('received %s', name.value)
#
#         # node = self.call_method('_render_csrf', [ctx_ref], lineno=lineno)
#         # return jinja2.nodes.CallBlock(node, [], [], [], lineno=lineno)
#         return self.call_method('_process', args, lineno=lineno)
#         # return jinja2.nodes.CallBlock(node, [], [], [], lineno=lineno)
#
#     def _process(self, context, args):
#         logger.info("process: %s, %s", context, args)
#         #csrf_token = context['csrf_token']
#         #return jinja2.Markup(self.template % unicode(csrf_token))
#         # return "BLAH< %s >" % context
#         # return jinja2.Markup('blah')
#         return 'tada'
#
# # csrf = CsrfExtension