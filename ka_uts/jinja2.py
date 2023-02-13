# coding=utf-8

import os
import jinja2

from ka_uts.yaml import Yaml


class Jinja2:
    """ Manage Object to Json file affilitation
    """
    @staticmethod
    def read_template(path: str) -> dict:
        dir, file = os.path.split(path)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(dir))
        return env.get_template(file)

    @classmethod
    def read(cls, path: str, **kwargs) -> dict:
        try:
            # read jinja template from file
            template = cls.read_template(path)

            # render template as yaml string
            template_rendered = template.render(**kwargs)

            # parse yaml string as dictionary
            dic = Yaml.load_with_safeloader(template_rendered)
            return dic
        except Exception:
            # logger = logging.getLogger(__name__)
            raise
