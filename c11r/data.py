# Technically this import could be optional, because not everyone needs YAML.
# If that becomes a requirement, surround this with a try/catch ImportError.
import logging

import jinja2.ext
import yaml
from jinja2 import TemplateNotFound
from os.path import isfile

logger = logging.getLogger(__name__)


class YamlDataLoader(object):
    extension = '.yml'

    def loadf(self, filename):
        """Load a YAML file and return a dictionary"""
        with open(filename) as f:
            r = yaml.load(f)
        ##print(r)
        return r

def yaml_to_template(filename):
    """Load the given YAML filename, and generate a Jinja template
    that sets variable(s) to represent that data.

    This is... not the most ideal solution.

    A more ideal solution would generate Jinja2 nodes representing
    the data, rather than load YAML then generate text then parse the
    text. Still, this is a pragmatic solution.
    """
    import io
    with open(filename) as f:
        data = yaml.load(f)

    out = io.StringIO()
    out.write('{# loaded YAML from %r #}\n' % filename)
    for k, v in data.items():
        out.write('{{% set {}={} %}}\n'.format(k, repr(v)))
    return out.getvalue()


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
        if template.endswith('.yml'):
            if not isfile(template):
                raise TemplateNotFound(template)

            contents = yaml_to_template(template)
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