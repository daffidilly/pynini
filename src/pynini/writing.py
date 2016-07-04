class TemplateFileWriter(object):
    """A writer that formats the template to a file."""

    def __init__(self):
        pass

    def write(self, template, context, out_path):
        template.stream(context).dump(out_path)