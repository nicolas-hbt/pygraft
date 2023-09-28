import warnings

warnings.filterwarnings("ignore")

import json
from owlready2 import *
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from tqdm.auto import tqdm
import os
from datetime import datetime
from pygraft.utils import reasoner


class SchemaBuilder:
    def __init__(self, class_info, relation_info, folder_name, format):
        """
        Initializes the SchemaBuilder class.

        Args:
            self (object): The instance of the SchemaBuilder.
            class_info (dict): A dictionary containing class information.
            relation_info (dict): A dictionary containing relation information.
            folder_name (str): The name of the folder to be created. If None, a folder with the current date and time will be created.
            format (str): The format of the output file. Can be either "xml" or "ttl".

        Returns:
            None
        """
        self.class_info = class_info
        self.relation_info = relation_info
        self.format = format
        self.initialize_folder(folder_name)
        self.save_dict()

    def initialize_folder(self, folder_name):
        """
        Initializes a folder for output files.

        Args:
            self (object): The instance of the SchemaBuilder.
            folder_name (str): The name of the folder to be created. If None, a folder with the current date and time will be created.

        Returns:
            None
        """
        output_folder = "output/"
        if folder_name is None:
            output_folder += datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        else:
            output_folder += folder_name

        self.directory = f"{output_folder}/"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_dict(self):
        """
        Saves the dictionary containing relation information and class information to JSON files.

        Args:
            self (object): The instance of the SchemaBuilder.

        Returns:
            None
        """
        rel_info = {}

        for k, v in self.relation_info.items():
            if k == "rel2patterns":
                rel_info["rel2patterns"] = {r: list(p) for r, p in self.relation_info[k].items()}
            elif k != "pattern2rels":
                rel_info[k] = v

        with open(f"{self.directory}relation_info.json", "w") as file:
            json.dump(rel_info, file, indent=4)

        class_dict = {k: list(v) if isinstance(v, set) else v for k, v in self.class_info.items()}

        with open(f"{self.directory}class_info.json", "w") as file:
            json.dump(class_dict, file, indent=4)

    def building_pipeline(self):
        """
        Initializes and builds the pipeline for creating the graph.

        This function initializes a new graph object and sets up the necessary namespaces for ontology, RDF, and RDFS.
        It binds the namespaces to the graph and adds the OWL ontology to the graph.
        It also adds the CC0 license URI to the ontology.
        After setting up the namespaces and ontology, it calls helper functions to add classes, relations, and test the schema.
        Finally, it prints a message indicating that the schema has been created.

        Args:
            self (object): The instance of the SchemaBuilder.

        Returns:
            None
        """
        self.graph = Graph()

        owl = Namespace("http://www.w3.org/2002/07/owl")
        rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns")
        rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema")
        self.schema = Namespace("http://pygraf.t/")

        self.graph.bind("owl", owl)
        self.graph.bind("rdf", rdf)
        self.graph.bind("rdfs", rdfs)
        self.graph.bind("sc", self.schema)

        ontology_uri = URIRef(self.schema)
        self.graph.add((ontology_uri, RDF.type, OWL.Ontology))
        cc0_license_uri = URIRef("https://creativecommons.org/publicdomain/zero/1.0/")
        self.graph.add((URIRef(ontology_uri), URIRef("http://purl.org/dc/terms/license"), cc0_license_uri))

        self.add_classes()
        self.add_relations()

        print(f"\nSchema created.")

        ontology_file = (
            f"{self.directory}schema.rdf" if self.format == "xml" else f"{self.directory}schema.{self.format}"
        )
        reasoner(resource_file=ontology_file, resource="schema")

    def add_classes(self):
        """
        Adds classes to the graph based on the given class info.

        Args:
            self (object): The instance of the SchemaBuilder.

        Returns:
            None
        """
        classes = self.class_info["classes"]
        class2superclass = self.class_info["direct_class2superclass"]
        class2disjoints = self.class_info["class2disjoints"]

        for c in tqdm(classes, desc="Writing classes", unit="classes", colour="red"):
            class_URI = URIRef(self.schema + str(c))

            self.graph.add((class_URI, RDF.type, OWL.Class))

            if c in class2superclass:
                sp = class2superclass[c]

                if sp == "owl:Thing":
                    self.graph.add((class_URI, RDFS.subClassOf, OWL.Thing))
                else:
                    self.graph.add((class_URI, RDFS.subClassOf, URIRef(self.schema + str(sp))))

            if c in class2disjoints:
                for c2 in class2disjoints[c]:
                    self.graph.add((class_URI, OWL.disjointWith, URIRef(self.schema + str(c2))))

        print("\n")

    def add_relations(self):
        """
        Adds relations to the graph based on the provided relation information.

        This function iterates through each relation and performs the following steps:
        1. Creates a relation URI using the schema and the relation ID.
        2. Adds the rdf:type property to the relation URI with a value of OWL.ObjectProperty.
        3. If the relation has associated patterns, it adds the corresponding OWL property types to the relation URI.
        4. If the relation is not reflexive, it adds the domain and range assertions to the relation URI.
        5. If the relation has an inverse, it adds the inverseOf property to the relation URI.
        6. If the relation has a superrelation, it adds the subPropertyOf property to the relation URI.
        7. Serializes the graph to the specified output file.

        Args:
            self (object): The instance of the SchemaBuilder.

        Returns:
            None
        """
        relations = self.relation_info["relations"]
        rel2patterns = self.relation_info["rel2patterns"]
        rel2dom = self.relation_info["rel2dom"]
        rel2range = self.relation_info["rel2range"]
        rel2inverse = self.relation_info["rel2inverse"]
        rel2superrel = self.relation_info["rel2superrel"]

        for r in tqdm(relations, desc="Writing relations", unit="relations", colour="red"):
            relation_URI = URIRef(self.schema + str(r))

            # rdf:type
            self.graph.add((relation_URI, RDF.type, OWL.ObjectProperty))

            if r in rel2patterns:
                for object_property in rel2patterns[r]:
                    if object_property == "owl:Symmetric":
                        self.graph.add((relation_URI, RDF.type, OWL.SymmetricProperty))
                    if object_property == "owl:Asymmetric":
                        self.graph.add((relation_URI, RDF.type, OWL.AsymmetricProperty))
                    if object_property == "owl:Reflexive":
                        if r in rel2dom and r in rel2range:
                            if rel2dom[r] == rel2range[r]:
                                continue
                            else:
                                self.graph.add((relation_URI, RDF.type, OWL.ReflexiveProperty))
                        else:
                            self.graph.add((relation_URI, RDF.type, OWL.ReflexiveProperty))
                    if object_property == "owl:Irreflexive":
                        self.graph.add((relation_URI, RDF.type, OWL.IrreflexiveProperty))
                    if object_property == "owl:Transitive":
                        self.graph.add((relation_URI, RDF.type, OWL.TransitiveProperty))
                    if object_property == "owl:Functional":
                        self.graph.add((relation_URI, RDF.type, OWL.FunctionalProperty))
                    if object_property == "owl:InverseFunctional":
                        self.graph.add((relation_URI, RDF.type, OWL.InverseFunctionalProperty))

            if r in rel2dom and "owl:Reflexive" not in rel2patterns[r]:
                # https://oborel.github.io/obo-relations/reflexivity/: "Reflexivity is incompatible with domain and range assertions."
                domain_URI = URIRef(self.schema + str(rel2dom[r]))
                self.graph.add((relation_URI, RDFS.domain, domain_URI))

            if r in rel2range and "owl:Reflexive" not in rel2patterns[r]:
                # https://oborel.github.io/obo-relations/reflexivity/: "Reflexivity is incompatible with domain and range assertions."
                range_URI = URIRef(self.schema + str(rel2range[r]))
                self.graph.add((relation_URI, RDFS.range, range_URI))

            if r in rel2inverse:
                r_inv = URIRef(self.schema + str(rel2inverse[r]))
                self.graph.add((relation_URI, OWL.inverseOf, r_inv))

            if r in rel2superrel:
                superrel = URIRef(self.schema + str(rel2superrel[r]))
                self.graph.add((relation_URI, RDFS.subPropertyOf, superrel))

        print("\n")

        output_file = f"{self.directory}schema.rdf" if self.format == "xml" else f"{self.directory}schema.{self.format}"
        self.graph.serialize(output_file, format=self.format)

    def test_schema(self):
        """
        Tests the schema by loading the ontology file and running a reasoner.

        Args:
            self (object): The instance of the SchemaBuilder.

        Returns:
            None
        """
        ontology_file = (
            f"{self.directory}schema.rdf" if self.format == "xml" else f"{self.directory}schema.{self.format}"
        )
        ontology = get_ontology(ontology_file)

        try:
            with ontology.load():
                sync_reasoner_hermit(infer_property_values=False, debug=True)
        except OwlReadyInconsistentOntologyError:
            print("Inconsistent ontology.")
