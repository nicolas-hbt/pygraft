.. _usage:

Advanced Usage
============

``main.py`` comes with many available parameters that are described in the :doc:`usage/parameters` section.
Alternatively, run ``python help.py`` to get the full description of parameters.
In the following, some examples are provided for illustrative purposes.

Advanced Schema Generation
---------------------------

Generate a schema with user-specified parameters:

.. code-block:: bash

    python main.py -g schema -o schema1 -c 150 -md 5 -ad 2.5 -ci 2.1 -r 150 -psr 0.1 -pir 0.2 -ptr 0.25

Advanced Knowledge Graph Generation
---------------------------

Based on a predefined schema, generate a knowledge graph with user-specified parameters:

.. code-block:: bash

    python main.py -g kg -o schema1 -e 1500 -t 7000 -rbr 1.0 -u 0.0 -ps both

Full Pipeline Generation
---------------------------

Generate both a schema and a knowledge graph underpinned by it:

.. code-block:: bash

    python main.py -g both -o schema2 -c 150 -md 5 -ad 2.5 -ci 2.1 -r 150 -psr 0.1 -pir 0.2 -ptr 0.25 -e 1500 -t 7000 -rbr 1.0 -u 0.0 -ps both

Using a .yml config file
---------------------------

Instead of specifying the args in the command-line, it is possible to load a .yml config file.
To do so, we provide an example in the ``config`` folder, names ``example.yml``.
It is recommended to simply copy-paste this file, rename it as you wish, and modify the parameters in it directly.
Ultimately, you can load this .yml file using the ``config`` parameter (short option: ``-conf``):

.. code-block:: bash

    python main.py -conf example.yml