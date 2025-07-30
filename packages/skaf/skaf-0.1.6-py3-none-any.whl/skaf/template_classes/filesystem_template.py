from typing import Generator
import os
import yaml
from pathlib import Path
from typing import Callable

from .base import BaseTemplate, TemplateProperties


class FilesystemTemplate(BaseTemplate):

    template_properties_filename = 'template_properties.yaml'
    variables_helper_filename = 'variables_helper.py'

    def __init__(self,
                 template_name: str,
                 template_dir: str,
                 ):
        self.template_dir = template_dir
        self.properties = self._load_properties()
        self.variables_helper: Callable[[dict], dict] = self._load_variables_helper()
        self.template_name = template_name

    def _load_properties(self) -> TemplateProperties:
        properties_filename = Path(self.template_dir) / Path(self.template_properties_filename)
        if not os.path.exists(properties_filename):
            raise FileNotFoundError(f"Template properties file '{properties_filename}' does not exist.")
        with open(properties_filename, 'r') as file:
            properties = yaml.safe_load(file)
        properties = properties or {}
        return properties

    def _load_variables_helper(self) -> Callable:
        variables_helper_filename = Path(self.template_dir) / Path(self.variables_helper_filename)
        if not os.path.exists(variables_helper_filename):
            return lambda d: d
        with open(variables_helper_filename, 'r') as file:
            code = file.read()
        exec_globals = {}
        exec(code, exec_globals)
        variables_helper = exec_globals.get('variables_helper')
        if not callable(variables_helper):
            raise ValueError(f"Variables helper in '{variables_helper_filename}' is not callable.")
        return variables_helper


    def documents(self) -> Generator[tuple[str, str], None, None]:
        """
        Yields tuples of (relpath, content) for each document in the template.
        """
        template_root = Path(self.template_dir) / "template"
        if not os.path.exists(template_root):
            raise FileNotFoundError(f"Template root directory '{template_root}' does not exist.")
        for root, dirs, files in os.walk(template_root):
            rel_root = Path(root).relative_to(template_root)
            for name in files:
                rel_path_template = rel_root / name
                abs_path_template = template_root / rel_path_template
                with open(abs_path_template, 'r') as file:
                    content = file.read()
                yield str(rel_path_template), content
                
