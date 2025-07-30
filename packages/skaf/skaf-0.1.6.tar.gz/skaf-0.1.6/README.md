# skaf

## Overview
skaf is a Python tool designed to simplify project scaffolding. It provides a simple interface for defining project templates that can be rendered with minimal effort. Here's a quick guide to installing and making templates:

## Installation

Ensure you have Python 3.10 or above. Install using pip:

```bash
pip install skaf
```

Alternatively, you can clone and install the local package:

```bash
git clone <repository-url>
cd skaf
pip install .
```

## Features

- Users can define project templates locally or in a git repo
- Simple CLI command to apply scaffolding
- Users can provide variable values via a yaml, environment variables, or interactively at the command line at scaffolding time.
- Variable values can be used in directory names

## Creating your own templates

1. **Create a template directory**  
   In skaf, templates are directories of files that may or may not contain templating blocks. The default templater is [jinja2](https://jinja.palletsprojects.com/en/stable/), which is a full-featured templating engine with advanced features. *(Note that skaf does not currently use jinja Loaders)*

   Any files that have a `.jinja` file suffix will be rendered. Otherwise, the file will be left as-is.

   All files should be placed in a directory structure that looks like:

   ```
   my-template-root/
      ├── template/
      │   └── [any files you want]
      ├── template_properties.yaml   # this is metadata. required.
      └── variables_helper.py        # optional
      
   ```

   For example, imagine I want to generate a customized hello world printer that is hard-coded to say hello to a specific person named John. I would create the following file:

   ```jinja
   # my-template-root/template/hello.py.jinja

   print("Hello {{ some_name }}!")
   ```

2. **Create a `template_properties.yaml`**  
   Next, we can declare metadata about the template. At this point, that primarily looks like declaring a list of variables that might have default values. There are a couple of other optional top-level fields as well:

   ```template_properties.yaml
   templater: jinja2  # default
   auto_use_defaults: false  # default
   custom_variables:
   - name: "some_name"
     type: "str"  # optional
     default: "World"  # optional
     description: Who are we saying hello to?  # optional
   ```

   For custom variables, the `type`, `default`, and `description` fields are optional. Only `name` is required.

   When rendering is run, you will be prompted to enter a value for the `some_name` variable or to accept the default value `World`. If we had instead specified that top-level value `auto_use_defaults: true`, then the templater would run without asking for input, and would provide `World` in as the value for `some_name`. (This particular behavior can also be overridden when invoking the CLI command.)

   The two top-level fields `templater` and `auto_use_defaults` are shown here with default values.

3. **(Optional) Create a `variables_helper.py`**  
   It may be the case that you want to use some user-provided variable values to derive some other template variable
   value. For this, you can create a python file outside your `template/` directory, next to `template_properties.yaml` called `variables_helper.py` and define a `variables_helper` function
   that has the following form:

   ```python
   # variables_helper.py

   def variables_helper(variables: dict) -> dict:
      ...
   ```

   The function should accept a dictionary of variable values and return a dict. For example, imagine that you were
   provided a `namespace` variable with a value like `"com.mydomain.example"` and you wanted to turn that into a directory path string like `"com/mydomain/example"`. You could define a variables helper function like:

   ```python
   # variables_helper.py

   def variables_helper(variables: dict) -> dict:
      variables["namespace_path"] = variables["namespace"].replace(".", "/")
   ```

   This particular use case could be helpful in a templating scenario where you declared a template directory like:
   
   ```
   my-template-root/
      ├── template/
            └──src/
               └──main/
                  └──java/
                     └── {{ namespace_path }}
                           └── MyClass.java
   ```

   When the user provides a namespace `com.mydomain.example`, the rendered template would look like

   ```
   my-template-root/
      ├── template/
            └──src/
               └──main/
                  └──java/
                     └──com/
                        └──mydomain/
                           └──example/
                              └── MyClass.java
   ```

## Command-line Usage

The CLI provides several flags and arguments to customize the initialization of a project with templates:

```bash
skaf <project_name> [options]
```

### Positional Arguments:
- `<project_name>`: The name of the project to create.

### Options:

#### Must have one of these  
- `-t, --template <template_name>`: Specify the name of the project template to use. Must proivde one of `--path`, `--template`, or `--git`.
- `-p, --path <template_directory>`: Provide the path to a local template directory. Must proivde one of `--path`, `--template`, or `--git`.
- `-g, --git <git_connection_string>`: Provide a git repo that has the template directory structure to be used as a template source. Must proivde one of `--path`, `--template`, or `--git`.

#### Entirely optional  
- `-o, --output <output_directory>`: Set the output directory for the project. Defaults to the current working directory.
- `--varfile <variables_filepath>`: Provide a filepath to a yaml file with key-values that provide variable values.
- `--overwrite`: Allow overwrite of existing project directory if it exists.
- `--auto-use-defaults`: Override the template properties' `auto_use_defaults` with an explicit value here.
- `--no-project-dir`: Do not create a top-level `<project_name>` directory, but scaffold all templates directly into the output directory.
- `--debug`: Enable debug mode, which will raise exceptions rather than catching them with a tidier output.

### Example Commands

1. **Creating a project with a template that is included in the package:**
   ```bash
   skaf my_project -t setuptools_pyproject
   ```

2. **Using a local, user-defined template:**
   ```bash
   skaf my_project -p /path/to/my/template
   ```

3. **Defining an Output Directory:**
   ```bash
   skaf my_project -o /path/to/output -p /path/to/my/template
   ```

## Development Dependencies

To contribute or run tests, install development dependencies:

```bash
pip install .[dev]
```

## Contribute

If you find a bug or have a feature request, please file an [issue](https://github.com/jdraines/skaf/issues).
