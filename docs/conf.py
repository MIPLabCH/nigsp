# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

from sphinx_gallery.sorting import FileNameSortKey

import nigsp

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "nigsp"
copyright = "2022, Stefano Moia, EPFL"
author = "Stefano Moia"

# Import project to get version info
sys.path.insert(0, os.path.abspath(os.path.pardir))

# The short X.Y version
version = nigsp.__version__
# The full version, including alpha/beta/rc tags
release = nigsp.__version__
package = nigsp.__name__
gh_url = "https://github.com/MIPLabCH/nigsp"

# -- General configuration ---------------------------------------------------

needs_sphinx = "2.0"  # based on setup.cfg requirements

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.import sphinx_rtd_theme  # noqa

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "myst_parser",
    "numpydoc",
    "sphinxarg.ext",
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinx_issues",
]

# Generate the API documentation when building
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": False,
    "exclude-members": "LGR",
}

numpydoc_show_class_members = False
autoclass_content = "class"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# Sphinx will warn about all references where the target cannot be found.
nitpicky = True
nitpick_ignore = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "furo"
html_show_sourcelink = False
html_show_sphinx = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ["_static"]
html_css_files = [
    "css/style.css",
]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "light_logo": "logos/nigsp_picto_circle_coral_background.svg",
    "dark_logo": "logos/nigsp_picto_circle_coral_background.svg",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": gh_url,
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    "sidebar_hide_name": True,
}

# html_favicon = '_static/logo.png'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "nigsp"

# -- intersphinx -------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}
intersphinx_timeout = 5

# -- sphinx-issues -----------------------------------------------------------
issues_github_path = gh_url.split("https://github.com/")[-1]

# -- autosectionlabels -------------------------------------------------------
autosectionlabel_prefix_document = True

# -- sphinxcontrib-bibtex ----------------------------------------------------
bibtex_bibfiles = []

# -- numpydoc ----------------------------------------------------------------
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = False

# x-ref
numpydoc_xref_param_type = True
numpydoc_xref_aliases = {
    # Matplotlib
    "Axes": "matplotlib.axes.Axes",
    "Figure": "matplotlib.figure.Figure",
    # Python
    "bool": ":class:`python:bool`",
    "Path": "pathlib.Path",
    "TextIO": "io.TextIOBase",
}
numpydoc_xref_ignore = {
    "of",
    "optional",
    "or",
    "shape",
}

# validation
# https://numpydoc.readthedocs.io/en/latest/validation.html#validation-checks
error_ignores = {
    "GL01",  # docstring should start in the line immediately after the quotes
    "EX01",  # section 'Examples' not found
    "ES01",  # no extended summary found
    "SA01",  # section 'See Also' not found
    "RT02",  # The first line of the Returns section should contain only the type, unless multiple values are being returned  # noqa
}
numpydoc_validate = True
numpydoc_validation_checks = {"all"} | set(error_ignores)
numpydoc_validation_exclude = {  # regex to ignore during docstring check
    r"\.__getitem__",
    r"\.__contains__",
    r"\.__hash__",
    r"\.__mul__",
    r"\.__sub__",
    r"\.__add__",
    r"\.__iter__",
    r"\.__div__",
    r"\.__neg__",
}

# -- sphinx-gallery ----------------------------------------------------------
sphinx_gallery_conf = {
    "backreferences_dir": "generated/backreferences",
    "doc_module": (f"{package}",),
    "examples_dirs": ["../tutorials"],
    "exclude_implicit_doc": {},  # set
    "filename_pattern": r"\d{2}_",
    "gallery_dirs": ["generated/tutorials"],
    "line_numbers": False,
    "plot_gallery": True,
    "reference_url": {f"{package}": None},
    "remove_config_comments": True,
    "show_memory": True,
    "within_subsection_order": FileNameSortKey,
}

# -- Generate API automagically -----------------------------------------------
def run_apidoc(_):
    from sphinx.ext.apidoc import main

    cur_dir = os.path.normpath(os.path.dirname(__file__))
    output_path = os.path.join(cur_dir, "api")
    modules = os.path.normpath(os.path.join(cur_dir, "../nigsp"))
    exclusions = [
        "../nigsp/tests/*",
        "../nigsp/cli/*",
    ]
    main(["-e", "-f", "-T", "-o", output_path, modules] + exclusions)


# -- Final Setup -------------------------------------------------------------

# https://github.com/rtfd/sphinx_rtd_theme/issues/117
# launch setup
def setup(app):  # noqa
    app.connect("builder-inited", run_apidoc)
    app.add_css_file("theme_overrides.css")
    app.add_js_file("https://cdn.rawgit.com/chrisfilo/zenodo.js/v0.1/zenodo.js")
