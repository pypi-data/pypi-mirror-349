# Installing pyDARM

It is recommended to first install [anaconda](https://www.anaconda.com/products/individual) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you have not already done so, as this simplifies your life installing/removing python modules without disrupting your existing environment.[^1] For example, some users may find it convenient to have the production version and development versions of pyDARM in different environments.

**Important: choose python version >=3.8 as earlier versions of python are not supported.**

## Packaged released version

For best results, please install from [conda-forge](https://conda-forge.org/):

```shell
conda install -c conda-forge pydarm
```

On Unix systems, you can also install directly from PyPI:

```shell
pip install pydarm
```

## Install from source in a conda environment

In order to use the latest version of the code, not yet released on PyPI or conda-forge, it will be necessary to download the latest version of the pyDARM repository. Either clone pyDARM directly (if you are not planning to do any development work) or fork-and-clone (if you plan to or sometime in the future plan to do any development). Change to the local git repository where the clone resides.
```shell
git clone <pyDARM git repository address>
cd pydarm
```

Once conda is installed and pyDARM has been cloned from source, create a new environment for pyDARM and install required packages
```shell
conda env create --name <pydarm-example> --file conda/environment.yaml
conda activate <pydarm-example>
```
Replace `<pydarm-example>` with a name you think is appropriate for yourself to remember what environment this is.

Next install pyDARM from source within the conda environment you just created.
```shell
python -m pip install .
```
pyDARM is now ready to use as a module for import in this environment. If you switch environments, then pyDARM will not be accessible as a module for import. If you have different local clones of pyDARM (different versions of the code) and you want to use those different versions, then they need to be installed into separate conda environments.

## Install from source for active development

If actively developing pyDARM, then it may be preferable to run
```shell
python -m pip install -e .
```
This installs pyDARM so that changes within the repository are immediately propagated into the code you run. You should rerun this command if you keep your feature branch up-to-date with the upstream repository (not strictly necessary--it is so that the `pydarm --version` command will display properly).

## Install on a remote cluster under jupyter notebook

Please see `examples/pydarm_example.ipynb` for instructions on installing to a jupyter notebook.


[^1]: Optionally, [mamba](https://mamba.readthedocs.io/en/stable/) may be used instead of conda.
