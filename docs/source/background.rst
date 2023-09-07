.. _background:

Background
============


Schemas
---------------------------
..
    - Definition + citation Gruber
    - Important Terms: Classes, Relations, Axioms, Properties, Relational Patterns, etc.
    - Toy Example
    - RDF, RDFS, OWL, etc (d'ailleurs comment les nommer ???)
    - Where to find domain-specific ontologies? => Links
    - The need/challenge for domain-agnostic ontologies => Melo 2017

A schema -- e.g. an ontology -- refers to a explicit specification of a conceptualization that includes concepts, properties, and restrictions within a particular domain of knowledge :cite:`gruber1995`. 
It helps ensure consistency, clarity, and interoperability when representing and sharing knowledge.
We consider schemas to be represented as a collection of concepts :math:`\mathcal{C}`, properties :math:`\mathcal{P}`, and axioms :math:`\mathcal{A}`, i.e. :math:`\mathcal{S} = \{ \mathcal{C}, \mathcal{P},  \mathcal{A}\}`.

..
    some example here (RDF triples)

They are typically represented using formal languages or vocabularies such as RDFS_ (Resource Description Framework Schema) and OWL_ (Web Ontology Language).

    
Knowledge Graphs
---------------------------
..
    - DIFFERENT Definitions + citations
    - Tell which one PyGraft follows
    - Important Terms
    - Toy Example
    - Benchmark KGs => links + citations

Regarding KGs, distinct definitions co-exist :cite:`bonatti`, :cite:`ehrlinger`. In this work, we stick to the inclusive definition of Hogan et al. :cite:`kgbook`, i.e. we consider a KG to be a graph where nodes represent entities and edges represent relations between these entities.
The link between schemas and KGs lies in the fact that schemas are often used to define the structure and semantics of a KG. In other words, a schema defines the vocabulary and rules that govern entities and relationships in a KG.
In this view, a KG is a data graph that can be potentially enhanced with a schema :cite:`kgbook`.

..
    some example here, such as BarackObama presidentOf USA

..
    some example here, such as presidentOF -rdfs:domain-> Person and rdfs:range-> Country
    

Graph Generation
---------------------------

The generation principle that underpins synthetic graph generators leads to differentiate three main families of generators: *stochastic-based*, *deep generative*, and *semantic-driven* ones.

Stochastic-based Generators
~~~~~
Stochastic-based generators are usually characterized by their ability to output large graphs in a short amount of time. 
Early works around the development of this family of generators are represented by the famous Erdős–Rényi model :cite:`erdos1959`, which is a foundational stochastic model for generating random graphs. 
The Erdős–Rényi model generates graphs by independently assigning edges between pairs of nodes with a fixed probability. 
The Barabási-Albert model :cite:`barabasi2002`, is another stochastic model that exhibits scale-free degree distributions. 
The Barabási-Albert model is based on the principle of preferential attachment, where new nodes are more likely to attach to nodes with higher degrees. 
The R-MAT model :cite:`rmat2004` is another well-known stochastic graph generator that generates large-scale power-law graphs with properties like power-law degree distributions, small-world characteristics, and community structures. 
More recently, TrillionG :cite:`trilliong2017` has been presented as an extension of R-MAT. TrillionG represents nodes and edges as vectors in a high-dimensional space. 
It captures the structural characteristics of real-world graphs and generates synthetic graphs that mimic the properties observed in those graphs. 
TrillionG allows users to generate large graphs up to trillions of edges while exhibiting lower space and time complexities than previously proposed generators.

Deep Generative Graph Generators
~~~~~
Another line of research revolves around the development of deep generative graph generators. 
These models are trained on existing graph datasets and learn to capture the underlying patterns and structures of the input graphs. 
Deep generative graph models are typically based on generative adversarial networks (GANs) and graph neural networks (GNNs), recurrent neural networks (RNNs), or variational autoencoders (VAEs). 
They often take into account both the structural and attribute information of the input graphs to generate new graphs that exhibit similar properties. 
GraphGAN :cite:`graphgan2018` leverages the GAN structure, in which the generative model receives a vertex and aims at fitting its true connectivity distribution over all other vertices -- thereby producing fake samples for the discriminative model to differentiate from ground-truth samples. 
GraphRNN :cite:`graphrnn2018` is a deep autoregressive model that trains on a collection of graphs. 
It can be viewed as a hierarchical model adding nodes and edges in a sequential manner: a graph-level RNN maintains the state of the graph and generates new nodes, while an edge-level RNN generates the edges for each newly generated node. 
A representant of the VAE family of generators is NeVAE :cite:`nevae2020`, which is specifically designed for molecular graphs. NeVAE features a decoder which is able to guarantee a set of valid properties in the generated molecules.

Semantic-driven Generators
~~~~~
Semantic-driven synthetic generators, in contrast, incorporate schema-based constraints or external knowledge to generate graphs that exhibit specific properties or follow certain patterns relevant to the given field of application.
In :cite:`guo2005`, the Lehigh University Benchmark (LUBM) and the Univ-Bench Artificial data generator (UBA) are presented. 
The latter is an ontology modelling the university domain while the latter aims at generating synthetic graphs based on the LUBM schema as well as user-defined queries and restrictions. 
Similarly, the Linked Data Benchmark Council (LDBC) :cite:`angles2014` released the Social Network Benchmark (SNB), which includes a graph generator for synthesizing social network data based on realistic distributions. 
gMark :cite:`bagan2017` has subsequently been presented as the first generator that satisfies the criteria of being domain-independent, extensible, schema-driven, and highly configurable, all at the same time. 
In :cite:`melo2017`, Melo and Paulheim focus on the synthesis of KGs for the purpose of benchmarking link prediction and type prediction tasks. 
The authors claim that there is a need for more diverse benchmark datasets for link prediction, with the possibility of having control over their characteristics (*e.g.* the number of entities, relation assertions, number of types, etc.). 
Therefore, Melo and Paulheim propose a synthesis approach which closely resemble real-world graphs while allowing for controlled variations in graph properties. 
Notably, they highlight the fact that most works focus on synthesizing KGs based on an existing schema, which leads them to formulate the desiderata of generating both a schema and KG from scratch as a promising venue for future work -- which PyGraft actually does. 
Subsequently, Feng *et al.* :cite:`feng2021` proposed a schema-driven graph generator based on the concept of Extended Graph Differential Dependencies (:math:`GDD^{x}`), which exhibits user-specified graph patterns, node attributes and degree distributions based on the graph's schema. 
The DLCC benchmark proposed in :cite:`portisch2022` features a synthetic KG generator based on user-specified graph and schema properties. 
Beyond asking for a given number of nodes, relations and degree distribution in the resulting KG, it allows for specifying a few RDFS_ constraints for the generation of the underpinning schema. 
To the best of our knowledge, this is the first and only work that allows to generate both a schema and a KG. 
However, the DLCC benchmark is specifically designed for the node classification task. Besides, only three RDFS_ assertions are taken into account, and the final logical consistency of the KG is not guaranteed.

    
.. _RDFS: https://www.w3.org/wiki/RDFS
.. _OWL: https://www.w3.org/OWL/