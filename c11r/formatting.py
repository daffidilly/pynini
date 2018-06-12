# -*- coding: utf-8 -*-
import logging
from os import walk
from os.path import splitext, isfile, isdir
from pathlib import Path

# from chainmap import ChainMap  # python 2.7 polyfill; uses Python 3 ChainMap if available
# from .utils import mkdir_p
# from .exceptions import SetupError


logger = logging.getLogger(__name__)


class Formatter(object):
    """Formats templates to HTML"""

    def __init__(self, setup):
        self.setup = setup
        self.output_dir = Path(self.setup.output_dir)  # TODO rename output_path
        # self.data = dict()

    def run(self):
        for path in (Path(path) for path in self.setup.paths):
            if path.is_file():
                self.process_file(path)
            elif path.is_dir():
                self.walk_src(path)
            else:
                logger.warning("Unrecognised file type: %s", str(path))

    def walk_src(self, path):
        logger.debug("walk_src: {}".format(path))
        for root, dirs, files in walk(path):
            root = Path(root)
            #logger.debug("walk_src root={}, dirs={}, files={}".format(root, dirs, files))
            for filename in files:
                self.process_file(filename_path=root / filename)

        logger.info("walk_src: DONE")

    def process_file(self, filename_path):  # , root: Path):
        # filename_path = root / filename
        # start, ext = splitext(filename)

        # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.stem
        start = filename_path.stem
        ext = filename_path.suffix
        logger.debug("process: {}-> {}".format(str(filename_path), ext))

        # find the right processor based on file extension, so 'jinja2' files
        # are processed by JinjaProcessor, for example.
        processor = self.setup.processor_for_ext(ext)

        output_filename = processor.get_output_filename(filename_path.parent, start, ext)
        output_rel_path = output_filename.relative_to(self.setup.src_dir)
        logger.info("Rel: %s", output_rel_path)

        output_path = self.output_dir / output_rel_path

        if output_path:
            logger.debug('-> %s (%s)', output_path, processor.name)
            # output_path = self.setup.output_dir + '/' + output_name
            logger.debug('=> final: %s', output_path)

            processor.process(self.setup, filename_path, output_path)
            # in above, write output to output_path, creating dirs with correct permissions
        else:
            logger.debug('-> no output for %s', filename_path)

            # if ext in self.setup.template_extensions:
            #     output_name = root + '/' + start  # substract the template extension
            #     logger.debug('-> a template into %s', output_name)
            # else:
            #     logger.debug('-> copy as is')

    # def load_data(self):
    #     # TODO DELETE THIS COMMENT AND LOGIC
    #     # # work in the parent of the pages directory, because we
    #     # # want the filenames to begin "pages/...".
    #     # chdir(dirname(self.setup.pages_dir))
    #     # rel = relpath(self.setup.pages_dir)
    #
    #     # TODO: probably delete all this data logic
    #
    #     for root, dirs, files in walk(self.setup.src_dir):
    #         for filename in files:
    #             start, ext = splitext(filename)
    #             if ext in self.setup.data_extensions:
    #                 loader = self.setup.data_loaders.get(ext)
    #                 path = join(root, filename)
    #                 if not loader:
    #                     raise SetupError("Identified data file '%s' by type '%s' but no loader found" % (filename, ext))
    #
    #                 data_key = join(root, start)
    #                 loaded_dict = loader.loadf(path)
    #                 self.data[data_key] = loaded_dict
    #
    #                 #self.setup.log.debug("data key [%s] ->" % (data_key, ), root, filename, ); pprint.pprint(loaded_dict, sys.stdout)
    #
    #     #pprint.pprint(self.data, sys.stdout)
    #     #print("XXXXX data:", self.data)

    # def transform_templates(self):
    #     empty = dict()
    #     try:
    #         global_context = ChainMap(self.data)
    #         for page in self.get_all_pages():
    #
    #             data_key, ext = splitext(page.file_path)
    #
    #             # The context is the complete set of variables the template
    #             # will be able to reference.
    #             #
    #             # There are automatic globals like 'root' and 'page'.
    #             #
    #             # There are variables scoped to the file, matched by name. So
    #             # if there is a file 'foo.yml' containing 'title=bar' then within
    #             # the template 'foo.html', the variable 'title' will be defined and
    #             # set to the string 'bar'.
    #
    #             file_variables = self.data.get(data_key) or empty
    #
    #             # print("XXX Data for %s:" % data_key)
    #             # pprint.pprint(file_variables, sys.stdout)
    #
    #             generator = file_variables.get('generator')
    #             if generator:
    #                 #print("XXX GENERATOR %s:" % data_key); pprint.pprint(generator, sys.stdout)
    #
    #                 data_file = generator.get('data_file')
    #                 iteration_list_key = generator.get('iteration_list_key')
    #                 iteration_item_key = generator.get('iteration_item_key', 'item')
    #                 output_filename = generator.get('output_filename')
    #
    #                 if data_file:
    #                     generator_data = self.data.get(data_file)
    #                     if not generator_data:
    #                         raise SetupError('%s generator data_file "%s" not found. Keys: %s' % (page.file_path, data_file, self.data.keys()))
    #
    #                 else:
    #                     generator_data = file_variables
    #
    #                 if iteration_list_key:
    #                     iteration_list = generator_data.get(iteration_list_key)
    #                     if not iteration_list:
    #                         raise SetupError('%s generator could not find key "%s" in generator data' % (page.file_path, iteration_list_key))
    #
    #                 #print("XXX ROOT %s:" % data_key); pprint.pprint(iteration_list, sys.stdout)
    #
    #                 if not output_filename:
    #                     raise SetupError('%s generator did not include output_filename' % (page.file_path,))
    #
    #                 page_name_template = self.setup.jinja.from_string(output_filename)
    #
    #                 for iteration_item in iteration_list:
    #                     #print("XXX ITERATION ITEM"); pprint.pprint(iteration_item, sys.stdout)
    #
    #                     # i love daddy
    #                     # automatic_variables = dict(
    #                     #     page=page.file_path,
    #                     #     root=page.relative_root_path,
    #                     # )
    #
    #                     context = global_context.new_child({
    #                         iteration_item_key: iteration_item,
    #                         iteration_list_key: iteration_list,
    #                         **file_variables,
    #                     })#.new_child(file_variables)
    #
    #                     page_name = page_name_template.render(context)
    #                     #print("XXX page_name_template=[%s] -> page_name=[%s]" % (output_filename, page_name))
    #
    #                     page.write(
    #                         out_path=join(self.setup.dist_dir, page_name),
    #                         context=context  # global_context.new_child(file_variables),
    #                     )
    #
    #             else:  # no generator
    #
    #                 page.write(
    #                     out_path=join(self.setup.dist_dir, page.output_file_path),
    #                     context=global_context.new_child(file_variables),
    #                 )
    #
    #                 # # Ensure the "pages" part of the path is trimed, so:
    #                 # #   "pages/index.html" -> ".../dist/index.html"
    #                 # #   "pages/about/foo.html" -> ".../dist/about/foo.html"
    #                 # out_path = join(self.config.dist_dir, page.output_file_path)
    #
    #     except jinja2.exceptions.TemplateSyntaxError as tse:
    #         self.setup.log.error("%s:%s: %s %s" % (tse.filename, tse.lineno, tse.name, tse.message))
    #         sys.exit(1)

    # def get_all_pages(self):
    #     # work in the parent of the pages directory, because we
    #     # want the filenames to begin "pages/...".
    #     #chdir(dirname(self.setup.pages_dir))
    #     rel = relpath(self.setup.pages_dir)
    #
    #     for root, dirs, files in walk(rel):  # self.config.pages_dir):
    #
    #         # examples:
    #         #
    #         #  root='pages'              root='pages/categories'
    #         #  dirs=['categories']       dirs=[]
    #         #  files=['index.html']      files=['list.html']
    #
    #         # self.setup.log.debug("\nTEMPLATE ROOT: %s" % root)
    #         # self.setup.log.debug("TEMPLATE DIRS: %s" % dirs)
    #         # self.setup.log.debug("TEMPLATE FILENAMES: %s" % files)
    #         # #dir_context = global_context.new_child(data_tree[root])
    #
    #         for filename in files:
    #             start, ext = splitext(filename)
    #             if ext in self.setup.template_extensions:
    #                 # if filename.endswith(".html"):  # TODO: should this filter be required at all?
    #                 yield Page(self.setup, filename, join(root, filename))

    # def walk_data_files(self, path):
    #     for root, dirs, files in walk(path):
    #         for filename in files:
    #             start, ext = splitext(filename)
    #             if ext in self.setup.data_extensions:
    #                 # if filename.endswith(".yml") or filename.endswith('.json') or filename.endswith('ini'):
    #                 yield root, dirs, filename

#
# class Page(object):
#     pages_path_prefix_pattern = re.compile('^/?pages/')
#
#     # dirname_pattern = re.compile('(^/+)')
#
#     def __init__(self, setup, file_name, file_path):
#         self.setup = setup
#         self.file_name = file_name
#         self.file_path = file_path
#
#         # Ensure the "pages" part of the path is trimed, so:
#         #   "pages/index.html" -> ".../dist/index.html"
#         #   "pages/about/foo.html" -> ".../dist/about/foo.html"
#         #
#         # ATM, trim the leading 'pages/'. I'm not sure if that
#         # will prove adequate over a longer term.
#         self.output_file_path = Page.pages_path_prefix_pattern.sub('', self.file_path)
#
#         # The "relative_root_path" is:
#         #   "pages/index.html" -> ""
#         #   "pages/about/foo.html" -> "../"
#         #   "pages/category/wool/product.html" -> "../../"
#         #
#         self.relative_root_path = '../' * self.output_file_path.count('/')
#         # Page.dirname_pattern.sub('..', self.output_file_path)
#
#     def write(self, out_path, context):
#         out_dir = dirname(out_path)
#         if not isdir(out_dir):
#             mkdir_p(out_dir, self.setup.mkdir_perms, exist_ok=True)
#
#         self.setup.log.info("format: %s (%s) -> %s" % (
#             self.file_name, self.file_path, out_path))
#
#         automatic_variables = dict(
#             page=self.file_path,
#             root=self.relative_root_path,
#         )
#
#         context = context \
#             .new_child(automatic_variables)
#
#         t = self.setup.jinja.get_template(self.file_path)
#
#         #t.stream(context).dump(out_path)
#         self.setup.template_writer.write(t, context, out_path)
