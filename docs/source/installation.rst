.. _installation:

Installation
============

.. note::
    In order to benefit from all the functionalities PyGraft offers, you need Java to be installed and the $JAVA_HOME environment variable to be properly assigned. This is because the HermiT reasoner currently runs using Java.

The latest stable version of PyGraft can be downloaded and installed from
`PyPI <https://pypi.org/project/pygraft>`_ with:

.. code-block:: bash

    $ pip install pygraft

The latest version of PyGraft can be installed directly from the
source on `GitHub <https://github.com/nicolas-hbt/pygraft>`_ with:

.. code-block:: bash

    $ pip install git+https://github.com/nicolas-hbt/pygraft.git

Please note that installing PyGraft will also set up the following Python dependencies:

.. code-block:: bash

    art
    matplotlib
    numpy
    pyyaml
    Owlready2
    rdflib
    tabulate
    tqdm

And that's it! You are all set! 
Before generating your first schemas and Knowledge Graphs (KGs), we recommend you to take a look at the :doc:`overview` section to get a better understanding of how PyGraft operates.
Not totally familiar with what schemas and KGs are? Consider going through the :doc:`background` section.
Next, you can jump to the :doc:`tutorial/first_steps` section to get a hands-on first experience with PyGraft.