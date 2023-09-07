.. _parameters:

Parameters
============

PyGraft allows for a broad range of user-specified parameters. Overall, these can be seen split into:

- general parameters, seen as metadata for the generation process
- schema parameters, governing the number of classes, relations, and how they are expected to interact
- KG parameters, governing the number of triples, instances, and how the latter should populate the schema

All these parameters can be freely modified in the ``json`` and ``yaml`` configuration files provided as templates.
For a quick example on how you can fetch the template in the current corkind directory and modify the parameters manually, see the :doc:`../tutorial/advanced` section.


Metadata
--------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - schema_name
     - Which schema to use
   * - format
     - Output format for the schema. Options: xml ttl nt


Schema Parameters
-----------------

Classes
~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - num_classes
     - Number of classes
   * - max_hierarchy_depth
     - Maximum hierarchy depth
   * - avg_class_depth
     - Average class depth
   * - class_inheritance_ratio
     - Class inheritance ratio
   * - avg_disjointness
     - Proportion of owl:DisjointWith

Relations
~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - num_relations
     - Number of relations
   * - relation_specificity
     - Relation specificity
   * - prop_profiled_relations
     - Proportion of rdfs:domain and rdfs:range
   * - profile_side
     - Whether profiled relations should have both a domain and a range or whether they should have at least one of them
   * - prop_symmetric_relations
     - Proportion of symmetric relations
   * - prop_inverse_relations
     - Proportion of owl:inverseOf
   * - prop_transitive_relations
     - Proportion of owl:TransitiveProperty
   * - prop_asymmetric_relations
     - Proportion of owl:AsymmetricProperty
   * - prop_reflexive_relations
     - Proportion of owl:ReflexiveProperty
   * - prop_irreflexive_relations
     - Proportion of owl:IrreflexiveProperty
   * - prop_subproperties
     - Proportion of rdfs:subPropertyOf
   * - prop_functional_relations
     - Proportion of owl:FunctionalProperty (not debugged)
   * - prop_inv_functional_relations
     - Proportion of owl:InverseFunctionalProperty (not debugged)

KG Parameters
-------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - num_entities
     - Number of entities
   * - num_triples
     - Number of triples
   * - relation_balance_ratio
     - Distribution of relations across triples
   * - prop_untyped_entities
     - Proportion of untyped entities
   * - avg_depth_specific_class
     - Average depth of most specific class for all entities
   * - multityping
     - Whether entities are multi-typed
   * - avg_multityping
     - Average number of most-specific classes that typed entities belong to
   * - format
     - Output format for the final graph

