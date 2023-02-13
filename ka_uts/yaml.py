# coding=utf-8

from pyaml import yaml as PyYaml


class Yaml:

    """ Manage Object to Yaml file affilitation
    """
    @staticmethod
    def load_with_loader(string: str):
        return PyYaml.load(string, Loader=PyYaml.Loader)

    @staticmethod
    def load_with_safeloader(string: str):
        return PyYaml.load(string, Loader=PyYaml.SafeLoader)

    @staticmethod
    def safe_load(string: str, **kwargs):
        return PyYaml.safe_load(string, **kwargs)
        # return PyYaml.load(string, Loader=PyYaml.SafeLoader)

    @staticmethod
    def read(path: str):
        with open(path) as fd:
            # The Loader parameter handles the conversion from YAML
            # scalar values to Python object format
            return PyYaml.load(fd, Loader=PyYaml.SafeLoader)
            # return PyYaml.load(fd, Loader=PyYaml.Loader)
        return None

    @staticmethod
    def write(obj, path: str):
        with open(path, 'w') as fd:
            PyYaml.dump(
                obj, fd,
                Dumper=PyYaml.SafeDumper,
                sort_keys=False,
                indent=4,
                default_flow_style=False
            )
            #   block_seq_indent=2,
