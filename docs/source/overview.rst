.. _overview:

Overview
=====

..
    - Forewords
    - Schema (Pipeline)
    - Class Generator
    - Relation Generator
    - KG Generator
    - Consistency Checking

We present PyGraft, a Python-based tool that allows generating highly parametrizable, domain-agnostic schemas and KGs. Importantly, the logical consistency of these schemas and KGs is checked using the HermiT reasoner.

The contributions of PyGraft are as follows:

- To the best of our knowledge, PyGraft is the first generator able to synthesize both schemas and KGs in a single pipeline.
- The generated schemas and KGs are described with an extended set of RDFS_ and OWL_ constructs, allowing for both fine-grained resource descriptions and strict compliance with common Semantic Web standards.
- A broad range of parameters can be specified by the user. These allow for creating an infinite number of graphs with different characteristics. More details on parameters can be found in the :doc:`../references/parameters` section.

From a high-level perspective, the entire PyGraft generation pipeline is depicted in Figure 1. 
In particular, Class and Relation Generators are initialized with user-specified parameters and used to build the schema incrementally. 
The logical consistency of the schema is subsequently checked using the HermiT reasoner from owlready2_.
If you are also interested in generating a KG based on this schema, the KG Generator is initialized with KG-related parameters and fused with the previously generated schema to sequentially build the KG. 
Ultimately, the logical consistency of the resulting KG is (again) assessed using HermiT.

.. figure:: /img/pygraft-overview.png
   :align: center

   Figure 1: PyGraft Overview

.. _RDFS: https://www.w3.org/wiki/RDFS
.. _OWL: https://www.w3.org/OWL/
.. _owlready2: https://github.com/pwin/owlready2/