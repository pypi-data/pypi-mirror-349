# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

from pydarm import __version__


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyDARM'
copyright = '2022, Evan Goetz'
author = 'Evan Goetz'
if "dev" in __version__:
    release = version = "dev"
else:
    release = version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

default_role = "obj"
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'numpydoc',
    'sphinx_immaterial_igwn',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial_igwn'
html_static_path = ['_static']
html_theme_options = {
    # metadata
    "edit_uri": "blob/main/docs",
    "repo_name": "pyDARM",
    "repo_type": "gitlab",
    "repo_url": "https://git.ligo.org/Calibration/pydarm",
    "icon": {
        "repo": "fontawesome/brands/gitlab",
        "edit": "material/file-edit-outline",
    },
    "features": [
        "navigation.sections",
    ],
    # colouring and light/dark mode
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "blue-grey",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/eye-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "amber",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/eye",
                "name": "Switch to light mode",
            },
        },
    ],
    # table of contents
    "toc_title_is_page_title": True,
}

# -- autodoc

autoclass_content = 'class'
autodoc_default_flags = ['show-inheritance', 'members', 'inherited-members']

# -- autosummary

autosummary_generate = True

# -- numpydoc

# fix numpydoc autosummary
numpydoc_show_class_members = False

# use blockquotes (numpydoc>=0.8 only)
numpydoc_use_blockquotes = True
