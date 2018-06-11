import logging
import shutil
from os import mkdir

from pathlib import Path

import jinja2
from jinja2 import Template

logger = logging.getLogger(__name__)


def ensure_dirs(output_path: Path, src_path: Path):
    """Ensure all directories in exist but, if not, make those
    directories and match permissions as listed in src_path.
    """
    logger.debug("ensure_dirs %s", output_path)
    logger.debug("  ref path: %s", src_path)
    output_dir = Path('.')
    ref_dir = Path('.')
    for d, r in zip(output_path.parts, src_path.parts):
        output_dir /= d
        ref_dir /= r
        logger.debug("    part: %s (%s) -> %s (%s)", d, r, output_dir, ref_dir)
        if not output_dir.is_dir():
            mkdir(output_dir)
            # copy permissions
            shutil.copystat(str(ref_dir), str(output_dir))


class DefaultProcessor:
    name = 'Copy as-is'

    def output_path(self, root_path, filename_base, filename_ext):
        return root_path / (filename_base + filename_ext)

    def process(self, env, src_file_path, output_file_path):
        logger.debug("==> Copy as is %s -> %s", src_file_path, output_file_path)
        ensure_dirs(output_file_path.parent, src_file_path.parent)
        shutil.copy2(src_file_path, output_file_path)


class JinjaProcessor(DefaultProcessor):
    name = 'Jinja'

    def output_path(self, root_path, filename_base, filename_ext):
        return root_path / filename_base  # no filename_ext

    def process(self, env, src_file_path: Path, output_file_path: Path):
        logger.debug("==> Jinja2 %s -> %s", src_file_path, output_file_path)
        ensure_dirs(output_file_path.parent, src_file_path.parent)

        try:
            # TODO: use ChainMap or more sophisticated system
            context = dict(
                meta=dict(
                    page=src_file_path,
                    **env.global_vars
                )
            )
            # with src_file_path.open() as src, output_file_path.open('w') as dest:
            with output_file_path.open('w') as dest:
                # template = env.jinja.from_string(src.read(), globals=None)
                src_path = str(src_file_path.relative_to(env.src_dir))
                logger.debug("==> Jinja2 src_path: %s", src_path)
                template = env.jinja.get_template(src_path, parent=None, globals=None)

                # env.jinja.template_writer.write(template, context, str(output_file_path))
                template.stream(context).dump(dest)
        except jinja2.exceptions.TemplateSyntaxError as tse:
            logger.error("%s:%s: %s %s", tse.filename, tse.lineno, tse.name, tse.message)
