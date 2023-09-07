.. _related:

.. raw:: html

   <style>
   .wy-nav-content {
       max-width: 1150px !important;
   }
   </style>

Related Libraries
=====================================

.. note::

   This section is under construction.

.. list-table:: Table 3. Feature comparison of graph generation tools. "NA" is used when a feature is not applicable due to the characteristics of the current generation tool. Domain-agnostic denotes whether a given tool is able to potentially operate with schemas of different application fields.
   :widths: 4 5 5 9 9 5 5 5
   :header-rows: 1
   :stub-columns: 0

   * - Tool
     - Domain-agnostic
     - Schema-driven
     - Schema generation
     - Schema properties
     - Graph properties
     - Scalable
     - Consistency check
   * - igraph_
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - NetworkX_
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - Snap_
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - GraphGen :cite:`graphgen2020`
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - GraphRNN :cite:`graphrnn2018`
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - GraphVAE :cite:`graphvae2018`
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:x:|
     - NA
   * - GraphWorld :cite:`palowitch2022`
     - |:heavy_check_mark:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - MolGAN :cite:`molgan2018`
     - |:x:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:x:|
     - NA
   * - NeVAE :cite:`nevae2020`
     - |:x:|
     - |:x:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - NA
   * - UBA-LUBM :cite:`guo2005`
     - |:x:|
     - |:heavy_check_mark:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - SNB :cite:`angles2014`
     - |:x:|
     - |:heavy_check_mark:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - Bagan *et al.* :cite:`bagan2017`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - Melo *et al.* :cite:`melo2017`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - :math:`GDD^{x}` :cite:`feng2021`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
     - NA
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - DLCC :cite:`portisch2022`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - 3
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - PyGraft (ours)
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - 13
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|

.. _igraph: https://github.com/igraph/python-igraph/
.. _NetworkX: https://github.com/networkx/networkx/
.. _Snap: https://github.com/snap-stanford/snap-python/
