import os
import yaml
from pathlib import Path
from git import Repo
import tempfile
from typing import Generator, Callable

from .base import BaseTemplate, TemplateProperties


class GitTemplate(BaseTemplate):
    template_properties_filename = 'template_properties.yaml'
    variables_helper_filename = 'variables_helper.py'

    def __init__(self, template_name: str, git_repo_path: str):
        self.template_name = template_name
        self._documents = {}
        
        # Use TemporaryDirectory as a context manager
        with tempfile.TemporaryDirectory() as temp_dir:
            Repo.clone_from(git_repo_path, temp_dir)
            self.properties = self._load_properties(temp_dir)
            self.variables_helper: Callable[[dict], dict] = self._load_variables_helper(temp_dir)
            self._load_documents(temp_dir)

    def _load_properties(self, temp_dir: str) -> TemplateProperties:
        properties_filename = Path(temp_dir) / self.template_properties_filename
        if not os.path.exists(properties_filename):
            raise FileNotFoundError(f"Template properties file '{properties_filename}' does not exist.")
        with open(properties_filename, 'r') as file:
            properties = yaml.safe_load(file)
        return properties or {}

    def _load_variables_helper(self, temp_dir) -> Callable:
        variables_helper_filename = Path(temp_dir) / Path(self.variables_helper_filename)
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

    def _load_documents(self, temp_dir: str):
        template_root = Path(temp_dir) / "template"
        if not template_root.exists():
            raise FileNotFoundError(f"Template root directory '{template_root}' does not exist.")
        for root, dirs, files in os.walk(template_root):
            rel_root = Path(root).relative_to(template_root)
            for name in files:
                rel_path_template = rel_root / name
                abs_path_template = template_root / rel_path_template
                with open(abs_path_template, 'r') as file:
                    content = file.read()
                self._documents[str(rel_path_template)] = content

    def documents(self) -> Generator[tuple[str, str], None, None]:
        """
        Yields stored (relpath, content) tuples from the document dictionary.
        """
        for relpath, content in self._documents.items():
            yield relpath, content
