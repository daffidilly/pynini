# Technically this import could be optional, because not everyone needs YAML.
# If that becomes a requirement, surround this with a try/catch ImportError.
import yaml


class YamlDataLoader(object):
    extension = '.yml'

    def loadf(self, filename):
        """Load a YAML file and return a dictionary"""
        with open(filename) as f:
            r = yaml.load(f)
        ##print(r)
        return r