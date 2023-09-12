.. _installation:

Installation & Setup
======================

This SDK is currently compatible with Python 3.6/3.7 and backwards-compatible with Python 2.7. However, future versions
may lose Python 2.7 compatibility due to official end of support of the Python 2 language on January 1, 2020. There are
a variety of ways to set up a Python 3 environment and install this library. For the sake of simplicity, a generalized
"basic" installation guide and a guide for users of the Anaconda Distribution are provided. The recommended setup for
all users (including those new to Python/coding) is that of the Anaconda distribution, as it is more prevalent in the
scientific and engineering community.


Setup Guide Using the Anaconda Distribution (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Anaconda Distribution is recommend if you are a scientist, engineer, researcher, or student. It comes bundled with
many useful Python scientific/numerical libraries, a GUI for managing the libraries, and several open-source software
development tools. Most importantly, just like the standard distribution of Python, it is free and open-source.

1. Install the latest version of the `Anaconda Distribution <https://www.anaconda.com/download/>`_, if not already installed.


2. (Optional, but recommended). Open the "Anaconda Prompt" terminal that comes with the Anaconda distribution, navigate to your project's directory and follow instructions for `creating a conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands>`_ and `activating a conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment>`_.


3. Install the :py:mod:`plantpredict` package to your environment by typing the command :code:`pip install plantpredict` into the terminal. (Note: :py:mod:`plantpredict` is not yet available via :code:`conda install`/the Anaconda Navigator GUI, but will be added to `conda-forge <https://conda-forge.org/>`_ in future versions).


4. Follow the steps in :ref:`authentication_oauth2` to obtain API credentials and authenticate with the server.


5. Use the tutorials in :ref:`example_usage` as a starting point for your own scripting and analysis. Detailed documentation on each class and method can be found in :ref:`sdk_reference`.

Basic Installation
^^^^^^^^^^^^^^^^^^

1. Install the `latest version of Python <https://www.python.org/downloads/>`_, if not already installed.


2. (Optional, but recommended) Create a virtual environment. Open a terminal/command prompt, navigate to your new project's directory, and follow the instructions for `installing and activating a virtualenv <https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv>`_.


3. Install :py:mod:`plantpredict` via `pip <https://pip.pypa.io/en/stable/>`_ by typing the command :code:`pip install plantpredict` into the terminal.


4. Follow the steps in :ref:`authentication_oauth2` to obtain API credentials and authenticate with the server.


5. Use the tutorials in :ref:`example_usage` as a starting point for your own scripting and analysis. Detailed documentation on each class and method can be found in :ref:`sdk_reference`.
