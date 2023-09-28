import copy
import time
import numpy as np
from collections import Counter
import json
import itertools
from owlready2 import *
from rdflib import Graph as RDFGraph, Namespace, URIRef, RDF, OWL
from tqdm.auto import tqdm
from pygraft.utils_kg import *
from pygraft.utils import reasoner


class InstanceGenerator:
    def __init__(self, **kwargs):
        self.init_params(**kwargs)
        self.init_utils(**kwargs)

    def init_params(self, **kwargs):
        """
        Initializes general KG information with user-specified parameters.

        Args:
            self (object): The instance of the InstanceGenerator.
            kwargs (dict): Dictionary of parameter names and values.

        Returns:
            None
        """
        self.schema = kwargs.get("schema")
        self.num_entities = kwargs.get("num_entities")
        self.num_triples = kwargs.get("num_triples")
        self.relation_balance_ratio = kwargs.get("relation_balance_ratio")
        self.prop_untyped_entities = kwargs.get("prop_untyped_entities")
        self.avg_depth_specific_class = kwargs.get("avg_depth_specific_class")
        self.multityping = kwargs.get("multityping")
        self.avg_multityping = kwargs.get("avg_multityping")
        self.multityping = False if self.avg_multityping == 0.0 else self.multityping

    def init_utils(self, **kwargs):
        """
        Initializes auxiliary information.

        Args:
            self (object): The instance of the InstanceGenerator.
            kwargs (dict): Dictionary of parameter names and values.

        Returns:
            None
        """
        self.directory = f"output/{self.schema}/"
        self.format = kwargs.get("format")
        self.fast_gen = kwargs.get("fast_gen")
        self.oversample = kwargs.get("oversample")
        self.fast_ratio = get_fast_ratio(self.num_entities) if self.fast_gen else 1
        self.oversample_every = int(self.num_triples / self.fast_ratio)
        self.load_schema_info()

    def load_schema_info(self):
        """
        Loads schema information from class_info and relation_info json files.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """

        with open(f"{self.directory}class_info.json", "r") as file:
            self.class_info = json.load(file)
        with open(f"{self.directory}relation_info.json", "r") as file:
            self.relation_info = json.load(file)

        if self.avg_depth_specific_class > (self.class_info["hierarchy_depth"] + 1):
            self.avg_depth_specific_class = self.class_info["hierarchy_depth"] - 1

    def assemble_instance_info(self):
        """
        Assembles the KG information and returns a dictionary
        containing statistics and user parameters.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            kg_info (dict): A dictionary containing information about the KG.
        """
        observed_entities = {entity for tup in self.kg for entity in tup[::2]}
        typed_observed = {entity for entity in observed_entities if entity in self.ent2classes_specific}
        observed_relations = {tup[1] for tup in self.kg}
        kg_info = {
            "user_parameters": {
                "schema": self.schema,
                "num_entities": self.num_entities,
                "num_triples": self.num_triples,
                "relation_balance_ratio": self.relation_balance_ratio,
                "prop_untyped_entities": self.prop_untyped_entities,
                "avg_depth_specific_class": self.avg_depth_specific_class,
                "multityping": self.multityping,
                "avg_multityping": self.avg_multityping,
            },
            "statistics": {
                "num_entities": len(observed_entities),
                "num_instantiated_relations": len(observed_relations),
                "num_triples": len(self.kg),
                "prop_untyped_entities": round(1 - (len(typed_observed) / len(observed_entities)), 2),
                "avg_depth_specific_class": self.current_avg_depth_specific_class,
                "avg_multityping": round(self.calculate_avg_multityping(), 2) if len(self.is_typed) > 0 else 0.0,
            },
        }

        with open(self.directory + "kg_info.json", "w") as file:
            json.dump(kg_info, file, indent=4)

        return kg_info

    def write_kg(self):
        """
        Writes the KG to a file.
        Initializes a new RDFGraph object and parses the schema.
        Each triple in the KG is added to the full graph.
        The full graph is then serialized to a file and checked for consistency.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        self.graph = RDFGraph()
        self.graph.parse(f"{self.directory}schema.rdf") if self.format == "xml" else self.graph.parse(
            f"{self.directory}schema.{self.format}"
        )

        schema = Namespace("http://pygraf.t/")
        self.graph.bind("sc", schema)

        for h, r, t in tqdm(self.kg, desc="Writing instance triples", unit="triples", colour="red"):
            self.graph.add((URIRef(schema + h), URIRef(schema + r), URIRef(schema + t)))

            if h in self.ent2classes_specific:
                for c in self.ent2classes_specific[h]:
                    self.graph.add((URIRef(schema + h), RDF.type, URIRef(schema + c)))

            if t in self.ent2classes_specific:
                for c in self.ent2classes_specific[t]:
                    self.graph.add((URIRef(schema + t), RDF.type, URIRef(schema + c)))

        self.graph.serialize(
            f"{self.directory}full_graph.rdf", format="xml"
        ) if self.format == "xml" else self.graph.serialize(
            f"{self.directory}full_graph.{self.format}", format=self.format
        )

        kg_file = (
            f"{self.directory}full_graph.rdf" if self.format == "xml" else f"{self.directory}full_graph.{self.format}"
        )
        reasoner(resource_file=kg_file, resource="KG")

    def generate_kg(self):
        self.pipeline()
        self.check_asymmetries()
        self.check_inverseof_asymmetry()
        self.check_dom_range()
        self.procedure_1()
        self.procedure_2()
        kg_info = self.assemble_instance_info()
        self.write_kg()

    def assign_most_specific(self):
        """
        Assigns the most specific class to each entity based on the hierarchy depth.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        hierarchy_depth = self.class_info["hierarchy_depth"] + 1
        shape = hierarchy_depth / (hierarchy_depth - 1)
        numbers = np.random.power(shape, size=len(self.is_typed))
        scaled_numbers = numbers / np.mean(numbers) * self.avg_depth_specific_class
        generated_numbers = np.clip(np.floor(scaled_numbers), 1, hierarchy_depth).astype(int)
        generated_numbers = [n if n < hierarchy_depth else hierarchy_depth for n in generated_numbers]
        self.current_avg_depth_specific_class = np.mean(generated_numbers)
        self.ent2layer_specific = {e: l for e, l in zip(self.is_typed, generated_numbers)}
        self.ent2classes_specific = {
            e: [np.random.choice(self.layer2classes[l])] for e, l in self.ent2layer_specific.items()
        }

    def complete_typing(self):
        """
        Completes the typing for the current entity (if multityping is enabled).

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        current_avg_multityping = 1.0
        entity_list = list(copy.deepcopy(self.is_typed))
        cpt = 0

        if entity_list:
            while current_avg_multityping < self.avg_multityping and cpt < 10:
                ent = np.random.choice(entity_list)
                most_specific_classes = self.ent2classes_specific[ent]
                specific_layer = self.ent2layer_specific[ent]
                compatible_classes = self.find_compatible_classes(most_specific_classes)
                specific_compatible_classes = list(
                    set(self.layer2classes[specific_layer]).intersection(set(compatible_classes))
                )
                specific_compatible_classes = [
                    cl for cl in specific_compatible_classes if cl not in most_specific_classes
                ]

                if specific_compatible_classes:
                    other_specific_class = np.random.choice(specific_compatible_classes)
                    self.ent2classes_specific[ent].append(other_specific_class)
                    current_avg_multityping = self.calculate_avg_multityping()
                    cpt = 0
                else:
                    cpt += 1

    def check_multityping(self):
        """
        Checks the multityping of entities and updates the badly typed entities.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        self.badly_typed = {}

        for e, classes in self.ent2classes_transitive.items():
            for c in classes:
                disj = self.class2disjoints_extended.get(c, [])
                if set(disj).intersection(classes):
                    self.badly_typed[e] = {"all_classes": classes, "problematic_class": c, "disjointwith": disj}
                    # keep only one of its most_specific classes and update its transitive classes
                    self.ent2classes_specific[e] = np.random.choice(self.ent2classes_specific[e])
                    self.ent2classes_transitive[e] = self.class_info["transitive_class2superclasses"][
                        self.ent2classes_specific[e]
                    ]
                    break

    def extend_superclasses(self):
        """
        Extends the superclasses of entities.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        self.ent2classes_transitive = {k: set(v) for k, v in self.ent2classes_specific.items()}

        for ent, specific_cls in self.ent2classes_specific.items():
            # Extend superclasses recursively
            for specific_cl in specific_cls:
                self.ent2classes_transitive[ent].update(
                    set(self.class_info["transitive_class2superclasses"][specific_cl])
                )
            self.ent2classes_transitive[ent] = list(set(self.ent2classes_transitive[ent]))

    def calculate_avg_multityping(self):
        """
        Calculates the average value of the multityping in the KG.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            float: The average value of multityping.
        """
        specific_cl_instanciations = len(list(itertools.chain(*self.ent2classes_specific.values())))
        return specific_cl_instanciations / len(self.is_typed)

    def find_compatible_classes(self, class_list):
        """
        Finds the classes that are compatible with the given class list.

        Args:
            self (object): The instance of the InstanceGenerator.
            class_list (list): A list of classes.

        Returns:
            set: A set of compatible classes.
        """
        disjoint_cls = set()

        for c in class_list:
            disjoint_cls.update(self.class2disjoints_extended.get(c, []))

        # Find all the classes that are not disjoint with any of the specific classes
        compatible_classes = [
            c
            for c in self.class2disjoints_extended.keys()
            if all(c not in self.class2disjoints_extended.get(specific_c, []) for specific_c in class_list)
        ]

        return set(compatible_classes) - set(class_list) | set(self.non_disjoint_classes)

    def pipeline(self):
        """
        Pipeline for processing entities and subsequently generating triples.

        Args:
            self (object): The instance of the InstanceGenerator.

        Return:
            None
        """

        if self.fast_gen:
            self.entities = [f"E{i}" for i in range(1, int(self.num_entities / self.fast_ratio) + 1)]
        else:
            self.entities = [f"E{i}" for i in range(1, self.num_entities + 1)]

        entities = copy.deepcopy(self.entities)
        np.random.shuffle(entities)

        threshold = int(len(self.entities) * (1 - self.prop_untyped_entities))
        self.is_typed = set(entities[:threshold])

        self.layer2classes = {int(k): v for k, v in self.class_info["layer2classes"].items()}
        self.class2layer = self.class_info["class2layer"]
        self.class2disjoints_extended = self.class_info["class2disjoints_extended"]
        self.classes = self.class_info["classes"]
        self.non_disjoint_classes = set(self.classes) - set(self.class2disjoints_extended.keys())

        self.assign_most_specific()

        if self.multityping:
            self.complete_typing()

        self.extend_superclasses()
        self.check_multityping()

        if self.fast_gen:
            ent2classes_spec_values = list(self.ent2classes_specific.values())
            ent2classes_trans_values = list(self.ent2classes_transitive.values())
            last_ent = len(self.entities)

            for _ in range(1, self.fast_ratio):
                entity_batch = [
                    f"E{i}" for i in range(last_ent + 1, last_ent + int(self.num_entities / self.fast_ratio) + 1)
                ]
                np.random.shuffle(entity_batch)
                threshold = int(len(entity_batch) * (1 - self.prop_untyped_entities))
                typed_entities = entity_batch[:threshold]
                self.is_typed.update(typed_entities)
                ent2classes_specific = {e: ent2classes_spec_values[idx] for idx, e in enumerate(typed_entities)}
                ent2classes_transitive = {e: ent2classes_trans_values[idx] for idx, e in enumerate(typed_entities)}
                self.ent2classes_specific.update(ent2classes_specific)
                self.ent2classes_transitive.update(ent2classes_transitive)
                self.entities += entity_batch
                last_ent = len(self.entities)

        self.generate_triples()

    def distribute_relations(self):
        """
        Distributes relations based on the number of triples and the relation balance ratio.

        Args:
            self (object): The instance of the InstanceGenerator.

        Return:
            None

        """
        self.num_relations = len(self.relation_info["relations"])

        if self.num_triples < self.num_relations:
            self.triples_per_rel = {f"R{i}": 1 if i < self.num_triples else 0 for i in range(self.num_relations)}
        else:
            mean = int(self.num_triples / len(self.relation_info["relations"]))
            spread_coeff = (1 - self.relation_balance_ratio) * mean
            self.relation_weights = generate_random_numbers(mean, spread_coeff, self.num_relations)
            self.triples_per_rel = {
                r: np.ceil(tpr)
                for r, tpr in zip(self.relation_info["relations"], np.array(self.relation_weights) * self.num_triples)
            }

    def generate_triples(self):
        """
        Generates triples for the KG.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        self.class2entities = {}

        for e, classes in self.ent2classes_transitive.items():
            for c in classes:
                self.class2entities.setdefault(c, []).append(e)

        self.class2unseen = copy.deepcopy(self.class2entities)
        self.flattened_unseen = list(set((itertools.chain(*self.class2entities.values()))))

        self.untyped_entities_priority = set(self.entities) - set(self.is_typed)
        self.untyped_entities = list(copy.deepcopy(self.untyped_entities_priority))

        self.rel2dom = self.relation_info["rel2dom"]
        self.rel2range = self.relation_info["rel2range"]
        self.rel2patterns = self.relation_info["rel2patterns"]

        self.kg = set()

        self.distribute_relations()

        self.last_oversample = 0

        attempt = 0
        while len(self.kg) < self.num_triples:
            rnd_r = np.random.choice(self.relation_info["relations"], p=self.relation_weights)
            new_triple = self.generate_one_triple(rnd_r)
            attempt += 1
            is_consistent = self.check_consistency(new_triple) if None not in new_triple else False
            if is_consistent:
                self.kg.add(new_triple)
                attempt = 0
            if attempt > 10:
                break

    def generate_one_triple(self, r):
        """
        Generates a single triple based on the given relation.

        Args:
            self (object): The instance of the InstanceGenerator.
            r (str): The relation for which to generate the triple.

        Returns:
            tuple: A tuple containing the head entity, relation, and tail entity of the generated triple.
        """
        r2dom = self.rel2dom.get(r)
        r2range = self.rel2range.get(r)
        token_dom, token_range = False, False

        if r2dom:
            h_list = self.class2unseen.get(r2dom, [])
            h = np.random.choice(h_list) if h_list else None
            if h is not None and self.check_class_disjointness(h, r2dom):
                token_dom = True
            else:
                is_valid = False
                attempt = 0
                while not is_valid and attempt < 10:
                    attempt += 1
                    class2entities = self.class2entities.get(r2dom, [])
                    if class2entities:
                        h = np.random.choice(class2entities)
                        is_valid = self.check_class_disjointness(h, r2dom)
                    else:
                        h = None
                if not is_valid:
                    h = None

        else:
            if len(self.untyped_entities) > 0:
                h = (
                    self.untyped_entities_priority.pop()
                    if self.untyped_entities_priority
                    else np.random.choice(self.untyped_entities)
                )
            else:
                h = np.random.choice(self.flattened_unseen)

        if r2range:
            t_list = self.class2unseen.get(r2range, [])
            t = np.random.choice(t_list) if t_list else None
            if t is not None and self.check_class_disjointness(t, r2range) and h is not None:
                self.class2unseen[r2range].remove(t)
                if token_dom and h in self.class2unseen[r2dom]:
                    self.class2unseen[r2dom].remove(h)
            else:
                is_valid = False
                attempt = 0
                while not is_valid and attempt < 10:
                    attempt += 1
                    class2entities = self.class2entities.get(r2range, [])
                    if class2entities:
                        t = np.random.choice(class2entities)
                        is_valid = self.check_class_disjointness(t, r2range)
                    else:
                        t = None
                if not is_valid:
                    t = None

        else:
            if len(self.untyped_entities) > 0:
                t = (
                    self.untyped_entities_priority.pop()
                    if self.untyped_entities_priority
                    else np.random.choice(self.untyped_entities)
                )
            else:
                t = np.random.choice(self.flattened_unseen)

        return (h, r, t)

    def check_consistency(self, triple):
        """
        Checks the consistency of a triple before adding it to the KG.

        Args:
            self (object): The instance of the InstanceGenerator.
            triple (tuple): A tuple representing a candidate triple (h, r, t).

        Returns:
            bool: True if the triple is consistent, False otherwise.
        """
        h, r, t = triple[0], triple[1], triple[2]

        if not h or not t:
            return False

        if r in self.relation_info["irreflexive_relations"] and h == t:
            return False

        if r in self.relation_info["asymmetric_relations"]:
            if h == t or (t, r, h) in self.kg:
                return False

        if r in self.relation_info["functional_relations"]:
            selected_triples = [triple for triple in self.kg if triple[:2] == (h, r)]
            if selected_triples:
                return False

        if r in self.relation_info["inversefunctional_relations"]:
            selected_triples = [triple for triple in self.kg if triple[1:] == (r, t)]
            if selected_triples:
                return False

        return True

    def check_inverseof_asymmetry(self):
        """
        Checks if the inverse-of-asymmetry condition holds for the given relations.

        This method checks if the inverse-of-asymmetry condition holds for each pair of relations (R1, R2)
        in the rel2inverse dictionary. The inverse-of-asymmetry condition states that if R1 is the inverse of R2,
        and either R1 or R2 is asymmetric, then the same (h, t) pair cannot be observed with both R1 and R2.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        rel2inverse = self.generate_rel2inverse()

        for r1, r2 in rel2inverse.items():
            if r1 in self.relation_info["asymmetric_relations"] or r2 in self.relation_info["asymmetric_relations"]:
                subset_kg = list(filter(lambda triple: triple[1] in (r1, r2), self.kg))

                if len(set(subset_kg)) < len(subset_kg):
                    counter = Counter(subset_kg)
                    duplicates = [h_t for h_t, count in counter.items() if count > 1]

                    for duplicate in duplicates:
                        self.kg.discard((duplicate[0], r1, duplicates[1]))

    def check_dom_range(self):
        """
        Checks the domain and range of triples in the KG and removes inconsistent triples.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        to_remove = set()

        for triple in self.kg:
            h, r, t = triple[0], triple[1], triple[2]
            r2dom, r2range = self.rel2dom.get(r), self.rel2range.get(r)
            if r2dom and h in self.ent2classes_transitive:
                is_valid = self.check_class_disjointness(h, r2dom)
                if not is_valid:
                    to_remove.add(triple)
            if r2range and t in self.ent2classes_transitive:
                is_valid = self.check_class_disjointness(t, r2range)
                if not is_valid:
                    to_remove.add(triple)

        self.kg -= to_remove

    def generate_rel2inverse(self):
        """
        Generates a dictionary containing pairs of inverse relations.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            rel2inverse (dict): A dictionary containing the inverse of the relation.
        """
        rel2inverse = self.relation_info["rel2inverse"]
        keys = list(rel2inverse.keys())
        values = list(rel2inverse.values())
        is_matching = all(keys[i] == values[i + 1] for i in range(0, len(keys), 2) if i + 1 < len(values))
        assert is_matching
        # because of the symmetric key-value pairs:
        rel2inverse = {k: v for i, (k, v) in enumerate(self.relation_info["rel2inverse"].items()) if i % 2 == 0}

        return rel2inverse

    def check_asymmetries(self):
        """
        Checks for asymmetries in the KG.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """

        for r in self.relation_info["asymmetric_relations"]:
            subset_kg = list(filter(lambda triple: triple[1] == r, self.kg))
            symmetric_dict = {}

            for triple in subset_kg:
                symmetric_triple = (triple[2], triple[1], triple[0])
                if symmetric_triple in subset_kg and symmetric_triple not in symmetric_dict.keys():
                    symmetric_dict[triple] = symmetric_triple

            to_remove = set(symmetric_dict.values())
            self.kg -= to_remove

    def check_class_disjointness(self, ent, expected_class):
        """
        Checks for class disjointness (owl:disjointWith) between domain/range of a relation
        and the classes to which belong the randomly sampled entity.

        Args:
            self (object): The instance of the InstanceGenerator.
            ent (str): The entity to check.
            expected_class (str): The expected class as domain or range of a relation.

        Returns:
            bool: True if the entity classes and expected class are disjoint, False otherwise.
        """
        classes_entity_side = self.ent2classes_transitive[ent]
        classes_relation_side = self.class_info["transitive_class2superclasses"][expected_class]

        for c in classes_relation_side:
            disj = self.class2disjoints_extended.get(c, [])
            if set(disj).intersection(set(classes_entity_side)):
                return False

        return True

    def oversample_triples_inference(self):
        """
        Infers new triples to be added to the KG based on logical deductions.
        Allows reaching user-specified number of triples without increasing the number of entities.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        used_relations = set()
        id2pattern = {
            1: self.relation_info["inverseof_relations"],
            2: self.relation_info["symmetric_relations"],
            3: self.relation_info["subrelations"],
        }
        attempt = 0

        while len(self.kg) < self.num_triples:
            attempt += 1
            chosen_id = np.random.randint(1, len(id2pattern) + 1)
            pattern2rels = id2pattern[chosen_id]
            np.random.shuffle(pattern2rels)

            if pattern2rels:
                rel = pattern2rels[0]

                if rel not in used_relations:
                    attempt = 0
                    used_relations.add(rel)
                    subset_kg = set([triple for triple in self.kg if triple[1] == rel])

                    if chosen_id == 1:
                        inv_rel = self.relation_info["rel2inverse"][rel]
                        inferred_triples = inverse_inference(subset_kg, inv_rel)

                    elif chosen_id == 2:
                        inferred_triples = symmetric_inference(subset_kg)

                    elif chosen_id == 3:
                        super_rel = self.relation_info["rel2superrel"][rel]
                        inferred_triples = subproperty_inference(subset_kg, super_rel)

                    # inferred_triples = inferred_triples[: 0.5 * int(len(inferred_triples))]
                    self.kg = self.kg | set(inferred_triples)

                    if len(self.kg) >= self.num_triples:
                        return

            if attempt > 1000:
                break

    def procedure_1(self):
        """
        Checks that domains and ranges are compatible with ent2classes_transitive of instantiated triples.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """

        for rel in self.rel2dom:
            if self.rel2dom[rel] in self.class2disjoints_extended:
                subset_kg = set([triple for triple in self.kg if triple[1] == rel])
                disjoint_with_dom = self.class2disjoints_extended[self.rel2dom[rel]]
                wrong_heads = set()
                for h, _, _ in subset_kg:
                    if h in self.ent2classes_transitive:
                        intersection = set(self.ent2classes_transitive[h]).intersection(disjoint_with_dom)
                        if intersection:
                            wrong_heads.add(h)

                problematic_triples = {
                    (head, relation, tail) for head, relation, tail in subset_kg if head in wrong_heads
                }
                self.kg -= problematic_triples

        for rel in self.rel2range:
            if self.rel2range[rel] in self.class2disjoints_extended:
                subset_kg = set([triple for triple in self.kg if triple[1] == rel])
                disjoint_with_range = self.class2disjoints_extended[self.rel2range[rel]]
                wrong_tails = set()
                for _, _, t in subset_kg:
                    if t in self.ent2classes_transitive:
                        intersection = set(self.ent2classes_transitive[t]).intersection(disjoint_with_range)
                        if intersection:
                            wrong_tails.add(t)

                problematic_triples = {
                    (head, relation, tail) for head, relation, tail in subset_kg if tail in wrong_tails
                }
                self.kg -= problematic_triples

    def procedure_2(self):
        """
        Checks if the inverse relationship between r1 and r2 satisfies certain conditions.

        Args:
            self (object): The instance of the InstanceGenerator.

        Returns:
            None
        """
        rel2inverse = self.generate_rel2inverse()
        for r1 in rel2inverse:
            r2 = rel2inverse[r1]
            subset_kg = set([triple for triple in self.kg if triple[1] == r1])
            if r2 in self.rel2range and self.rel2range[r2] in self.class2disjoints_extended:
                range_r2 = self.rel2range[r2]
                disjoint_with = self.class2disjoints_extended[range_r2]
                wrong_heads = set()
                for h, _, _ in subset_kg:
                    if h in self.ent2classes_transitive:
                        intersection = set(self.ent2classes_transitive[h]).intersection(disjoint_with)
                        if intersection:
                            wrong_heads.add(h)

                problematic_triples = {
                    (head, relation, tail) for head, relation, tail in subset_kg if tail in wrong_heads
                }
                self.kg -= problematic_triples

            if r2 in self.rel2dom and self.rel2dom[r2] in self.class2disjoints_extended:
                dom_r2 = self.rel2dom[r2]
                disjoint_with = self.class2disjoints_extended[dom_r2]
                wrong_tails = set()
                for _, _, t in subset_kg:
                    if t in self.ent2classes_transitive:
                        intersection = set(self.ent2classes_transitive[t]).intersection(disjoint_with)
                        if intersection:
                            wrong_tails.add(t)

                problematic_triples = {
                    (head, relation, tail) for head, relation, tail in subset_kg if tail in wrong_tails
                }
                self.kg -= problematic_triples
