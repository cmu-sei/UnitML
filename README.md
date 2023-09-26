<!--
 UnitML
 Copyright 2023 Carnegie Mellon University.
 NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
 Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
 [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
 This Software includes and/or makes use of Third-Party Software each subject to its own license.
 DM23-0976
-->


# UnitML

A JupyterLab extension used to generate pytest unit tests for a machine learning model.
The tool relies on the v1.2 TEC Descriptors, specifically the Data Pipeline and Trained Model descriptors.
Tests are generated based on the input and output specification contained within these descriptors.

This extension is composed of a Python package named `unitml`
for the server extension and a NPM package named `unitml`
for the frontend extension.

## Requirements

- JupyterLab >= 3.0
- pytest >= 7.4.2
- Pillow >= 10.0.1

## Install

To install the extension, download `.whl` file and execute:

```bash
conda create -n unitml-env jupyterlab
conda activate unitml-env
pip install unitml-0.1.0-py3-none-any.whl
jupyter lab
```

## Usage

Once installed, the extension will be added to Jupyter Lab and can be
ran by using the command `UnitML` in the Command Palette. The descriptors
must be located in the directory that Jupyter Lab is started in, or the 
extension will be unable to find them.

Once the tool has been ran, it will generate the file `test_generated.py` in
the directory with the descriptors. This file contains a framework for unit
testing the model specified.

While most of the file is ready to go, there are a couple sections that require
input from the user in order to work. These sections are marked with comments
starting with `# USER INPUT` and give an explanation of what needs to be added.

Once these sections have been updated, the tests are ready to be ran. Ensure that
the data pipeline and model files are available to be imported by the test file and run the tests.
Pytest can be run with the command, which will run all the tests contained in the file.

```bash
pytest
```

If desired, this can also be done within a jupyter notebook to preserve the output:

```python
import subprocess
subprocess.run["pytest"]
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall unitml
```

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the unitml directory
# Install package in development mode
pip install -e ".[test]"
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable unitml
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable unitml
pip uninstall unitml
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `unitml` within that folder.

### Testing the extension

#### Server tests

This extension is using [Pytest](https://docs.pytest.org/) for Python code testing.

Install test dependencies (needed only once):

```sh
pip install -e ".[test]"
# Each time you install the Python package, you need to restore the front-end extension link
jupyter labextension develop . --overwrite
```

To execute them, run:

```sh
pytest -vv -r ap --cov unitml
```

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro/) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
