import numpy as np
import random
from collections import defaultdict
import json
import itertools
import pkg_resources
from tabulate import tabulate


class RelationGenerator:
    def __init__(self, **kwargs):
        """
        Initializes the RelationGenerator.

        Args:
            self (object): The instance of the RelationGenerator.
            **kwargs: Additional keyword arguments.

        Keyword Args:
            class_info (dict): A dictionary containing information about the classes.
            num_relations (int): The number of relations to generate.
            relation_specificity (float): The desired specificity of the relations.
            prop_profiled_relations (float): The desired proportion of profiled relations.
            profile_side (str): The side to profile relations on.
            verbose (bool): Whether to print the relation schema.
            prop_symmetric_relations (float): The desired proportion of symmetric relations.
            prop_inverse_relations (float): The desired proportion of inverse relations.
            prop_functional_relations (float): The desired proportion of functional relations.
            prop_inverse_functional_relations (float): The desired proportion of inverse functional relations.
            prop_transitive_relations (float): The desired proportion of transitive relations.
            prop_subproperties (float): The desired proportion of subproperties.
            prop_reflexive_relations (float): The desired proportion of reflexive relations.
            prop_irreflexive_relations (float): The desired proportion of irreflexive relations.
            prop_asymmetric_relations (float): The desired proportion of asymmetric relations.

        Returns:
            None
        """
        self.init_params(**kwargs)
        self.init_property_props(**kwargs)
        self.init_relations()
        self.get_one_rel_compatibilities()
        self.get_inverseof_compatibilities()

    def init_params(self, **kwargs):
        """
        Initializes general relation information with user-specified parameters.

        Args:
            self (object): The instance of the RelationGenerator.
            **kwargs: Additional keyword arguments.

        Keyword Args:
            class_info (dict): A dictionary containing information about the classes.
            num_relations (int): The number of relations to generate.
            relation_specificity (float): The desired specificity of the relations.
            prop_profiled_relations (float): The desired proportion of profiled relations.
            profile_side (str): The side to profile relations on.
            verbose (bool): Whether to print the relation schema.
            prop_symmetric_relations (float): The desired proportion of symmetric relations.
            prop_inverse_relations (float): The desired proportion of inverse relations.
            prop_functional_relations (float): The desired proportion of functional relations.
            prop_inverse_functional_relations (float): The desired proportion of inverse functional relations.
            prop_transitive_relations (float): The desired proportion of transitive relations.
            prop_subproperties (float): The desired proportion of subproperties.
            prop_reflexive_relations (float): The desired proportion of reflexive relations.
            prop_irreflexive_relations (float): The desired proportion of irreflexive relations.
            prop_asymmetric_relations (float): The desired proportion of asymmetric relations.

        Returns:
            None
        """
        self.class_info = kwargs.get("class_info")
        self.num_relations = kwargs.get("num_relations")
        self.relation_specificity = kwargs.get("relation_specificity")
        self.prop_profiled_relations = kwargs.get("prop_profiled_relations")
        self.profile_side = kwargs.get("profile_side")
        self.verbose = kwargs.get("verbose")

    def init_property_props(self, **kwargs):
        """
        Initializes proportions of relation properties with user-specified parameters.

        Args:
            self (object): The instance of the RelationGenerator.
            **kwargs: Additional keyword arguments.

        Keyword Args:
            class_info (dict): A dictionary containing information about the classes.
            num_relations (int): The number of relations to generate.
            relation_specificity (float): The desired specificity of the relations.
            prop_profiled_relations (float): The desired proportion of profiled relations.
            profile_side (str): The side to profile relations on.
            verbose (bool): Whether to print the relation schema.
            prop_symmetric_relations (float): The desired proportion of symmetric relations.
            prop_inverse_relations (float): The desired proportion of inverse relations.
            prop_functional_relations (float): The desired proportion of functional relations.
            prop_inverse_functional_relations (float): The desired proportion of inverse functional relations.
            prop_transitive_relations (float): The desired proportion of transitive relations.
            prop_subproperties (float): The desired proportion of subproperties.
            prop_reflexive_relations (float): The desired proportion of reflexive relations.
            prop_irreflexive_relations (float): The desired proportion of irreflexive relations.
            prop_asymmetric_relations (float): The desired proportion of asymmetric relations. 

        Returns:
            None
        """
        self.prop_symmetric_relations = kwargs.get("prop_symmetric_relations")
        self.prop_inverse_relations = kwargs.get("prop_inverse_relations")
        self.prop_functional_relations = kwargs.get("prop_functional_relations")
        self.prop_inverse_functional_relations = kwargs.get("prop_inverse_functional_relations")
        self.prop_transitive_relations = kwargs.get("prop_transitive_relations")
        self.prop_subproperties = kwargs.get("prop_subproperties")
        self.prop_reflexive_relations = kwargs.get("prop_reflexive_relations")
        self.prop_irreflexive_relations = kwargs.get("prop_irreflexive_relations")
        self.prop_asymmetric_relations = kwargs.get("prop_asymmetric_relations")

    def init_relations(self):
        """
        Initializes the relations.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        self.relations = [f"R{i}" for i in range(1, self.num_relations + 1)]
        self.rel2dom = {}
        self.rel2range = {}
        self.unprofiled_relations = {}
        self.rel2inverse = {}
        self.inverseof_relations = []

    def generate_relation_schema(self):
        """
        Generates the relation schema.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            relation_info (dict): The assembled relation information.
        """
        self.generate_relations()

        if self.verbose:
            self.print_schema()

        relation_info = self.assemble_relation_info()

        return relation_info

    def assemble_relation_info(self):
        """
        Assembles and returns information about the relations.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            relation_info (dict): A dictionary containing statistics about the relations.
        """
        num_relations = len(self.relations)
        prop_reflexive = round(len(self.reflexive_relations) / num_relations, 2)
        prop_irreflexive = round(len(self.irreflexive_relations) / num_relations, 2)
        prop_functional = round(len(self.functional_relations) / num_relations, 2)
        prop_inversefunctional = round(len(self.inversefunctional_relations) / num_relations, 2)
        prop_symmetric = round(len(self.symmetric_relations) / num_relations, 2)
        prop_asymmetric = round(len(self.asymmetric_relations) / num_relations, 2)
        prop_transitive = round(len(self.transitive_relations) / num_relations, 2)
        prop_inverseof = round(len(self.inverseof_relations) / num_relations, 2)
        prop_subpropertyof = round(2 * len(self.prop2superprop) / num_relations, 2)
        prop_profiled_relations = round(self.current_profile_ratio, 2)
        relation_specificity = round(self.calculate_relation_specificity(), 2)

        relation_info = {
            "statistics": {
                "num_relations": num_relations,
                "prop_reflexive": prop_reflexive,
                "prop_irreflexive": prop_irreflexive,
                "prop_functional": prop_functional,
                "prop_inversefunctional": prop_inversefunctional,
                "prop_symmetric": prop_symmetric,
                "prop_asymmetric": prop_asymmetric,
                "prop_transitive": prop_transitive,
                "prop_inverseof": prop_inverseof,
                "prop_subpropertyof": prop_subpropertyof,
                "prop_profiled_relations": prop_profiled_relations,
                "relation_specificity": relation_specificity,
            },
            "relations": self.relations,
            "rel2patterns": self.rel2patterns,
            "pattern2rels": self.pattern2rels,
            "reflexive_relations": self.reflexive_relations,
            "irreflexive_relations": self.irreflexive_relations,
            "symmetric_relations": self.symmetric_relations,
            "asymmetric_relations": self.asymmetric_relations,
            "functional_relations": self.functional_relations,
            "inversefunctional_relations": self.inversefunctional_relations,
            "transitive_relations": self.transitive_relations,
            "inverseof_relations": self.inverseof_relations,
            "subrelations": self.subproperties,
            "rel2inverse": self.rel2inverse,
            "rel2dom": self.rel2dom,
            "rel2range": self.rel2range,
            "rel2superrel": self.prop2superprop,
        }

        return relation_info

    def generate_relations(self):
        """
        Generates relations and adds various properties to them.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        self.rel2patterns = {
            r: set() for r in self.relations
        }  # contains current ObjectProperties for each generated relation
        self.pattern2rels = {tuple(sorted(p)): set() for p in self.one_rel_compatibilities}

        self.reflexive_relations = random.sample(
            self.relations, k=int(len(self.relations) * self.prop_reflexive_relations)
        )
        self.update_rel2patterns("owl:Reflexive")
        self.irreflexive_relations = random.sample(
            list(set(self.relations) - set(self.reflexive_relations)),
            k=int(len(self.relations) * self.prop_irreflexive_relations),
        )
        self.update_rel2patterns("owl:Irreflexive")

        self.add_property("owl:Symmetric")
        self.add_property("owl:Asymmetric")
        self.add_property("owl:Transitive")
        self.add_property("owl:Functional")
        self.add_property("owl:InverseFunctional")

        self.add_inverseof()

        self.class2disjoints_extended = self.class_info["class2disjoints_extended"]
        self.layer2classes = self.class_info["layer2classes"]
        self.class2layer = self.class_info["class2layer"]

        # Reflexivity is incompatible with domain and range assertions
        self.unprofiled_relations["both"] = [r for r, p in self.rel2patterns.items() if "owl:Reflexive" not in p]
        self.unprofiled_relations["dom"] = [r for r, p in self.rel2patterns.items() if "owl:Reflexive" not in p]
        self.unprofiled_relations["range"] = [r for r, p in self.rel2patterns.items() if "owl:Reflexive" not in p]
        self.num_relations_wo_reflexive = len(self.unprofiled_relations["both"])

        self.current_profile_ratio = 0.0

        while self.current_profile_ratio < self.prop_profiled_relations:
            self.add_one_relation_profile()
            self.current_profile_ratio = (len(self.rel2dom) + len(self.rel2range)) / (
                2 * self.num_relations_wo_reflexive
            )

        self.add_property("rdfs:subPropertyOf")

    def calculate_profile_ratio(self):
        """
        Calculates the profile ratio.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            float: The calculated profile ratio.
        """
        return (len(self.rel2dom) + len(self.rel2range)) / (2 * len(self.relations))

    def add_one_relation_profile(self):
        """
        Adds one relation profile based on the value of `profile_side`.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        if self.profile_side == "both":
            self.add_complete_relation_profile()
        elif self.profile_side == "partial":
            self.add_partial_relation_profile()

    def add_partial_relation_profile(self):
        """
        Generates a partial relation profile by assigning a domain/range to a relation.
        This function selects a relation (either from the "domain" or "range" category)
        that has not been profiled yet and assigns a randomly sampled class to it. The
        function also updates the relation-specificity based on the chosen class. If the
        selected relation is transitive or symmetric, the function also assigns the
        sampled class to the corresponding "range" or "domain" relation. If the selected
        relation has an inverse relation, the function assigns the inverse relation the
        same class as the selected relation, as long as it is not reflexive.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        current_rel_specificity = self.calculate_relation_specificity()
        sampled_class = self.sample_class(current_rel_specificity)
        domain_or_range = "domain" if random.random() < 0.5 else "range"

        if domain_or_range == "domain":
            rel = self.unprofiled_relations["dom"].pop(0)
            rel2patterns = self.rel2patterns[rel]
            self.rel2dom[rel] = sampled_class

            if "owl:Transitive" in rel2patterns or "owl:Symmetric" in rel2patterns:
                self.rel2range[rel] = sampled_class
                if rel in self.unprofiled_relations["range"]:
                    self.unprofiled_relations["range"].remove(rel)
                    if rel in self.rel2inverse:
                        inverse_rel = self.rel2inverse[rel]
                        self.unprofiled_relations["dom"].remove(
                            inverse_rel
                        ) if inverse_rel in self.unprofiled_relations["dom"] else None
                        self.rel2dom[inverse_rel] = self.rel2range[rel]

            if rel in self.rel2inverse:
                inverse_rel = self.rel2inverse[rel]
                # if inverse_rel in self.unprofiled_relations["range"] and "owl:Reflexive" not in self.rel2patterns[inverse_rel]:
                self.unprofiled_relations["range"].remove(inverse_rel) if inverse_rel in self.unprofiled_relations[
                    "range"
                ] else None
                self.rel2range[inverse_rel] = self.rel2dom[rel]

        else:
            rel = self.unprofiled_relations["range"].pop(0)
            rel2patterns = self.rel2patterns[rel]
            self.rel2range[rel] = sampled_class

            if "owl:Transitive" in rel2patterns or "owl:Symmetric" in rel2patterns:
                self.rel2dom[rel] = sampled_class
                if rel in self.unprofiled_relations["dom"]:
                    self.unprofiled_relations["dom"].remove(rel)
                    if rel in self.rel2inverse:
                        inverse_rel = self.rel2inverse[rel]
                        self.unprofiled_relations["range"].remove(
                            inverse_rel
                        ) if inverse_rel in self.unprofiled_relations["range"] else None
                        self.rel2range[inverse_rel] = self.rel2dom[rel]

            if rel in self.rel2inverse:
                inverse_rel = self.rel2inverse[rel]
                # if inverse_rel in self.unprofiled_relations["dom"] and "owl:Reflexive" not in self.rel2patterns[inverse_rel]:
                self.unprofiled_relations["dom"].remove(inverse_rel) if inverse_rel in self.unprofiled_relations[
                    "dom"
                ] else None
                self.rel2dom[inverse_rel] = self.rel2range[rel]

    def add_complete_relation_profile(self):
        """
        Generates a complete relation profile by assigning a domain and a range to a relation.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        current_rel_specificity = self.calculate_relation_specificity()
        sampled_domain = self.sample_class(current_rel_specificity)
        rel = self.unprofiled_relations["both"].pop(0)
        rel2patterns = self.rel2patterns[rel]

        if "owl:Reflexive" not in rel2patterns:
            self.rel2dom[rel] = sampled_domain
            current_rel_specificity = self.calculate_relation_specificity()
            if "owl:Transitive" in rel2patterns or "owl:Symmetric" in rel2patterns:
                self.rel2range[rel] = sampled_domain
            else:
                sampled_range = self.sample_class_constrained(current_rel_specificity, sampled_domain)
                self.rel2range[rel] = sampled_range

            if rel in self.rel2inverse:
                inverse_rel = self.rel2inverse[rel]

                if inverse_rel in self.unprofiled_relations["both"]:
                    self.unprofiled_relations["both"].remove(inverse_rel)

                self.rel2dom[inverse_rel] = self.rel2range[rel]
                self.rel2range[inverse_rel] = self.rel2dom[rel]

    def calculate_relation_specificity(self):
        """
        Calculates the specificity of relations.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        domains = list(self.rel2dom.values())
        ranges = list(self.rel2range.values())
        both = domains + ranges

        return np.mean([self.class2layer[c] for c in both])

    def sample_class(self, current_rel_specificity):
        """
        Takes in a current relative specificity value
        and returns a random class from a list of filtered classes
        such that the current relative specificity value converges towards user-specified value.

        Args:
            self (object): The instance of the RelationGenerator.
            current_rel_specificity (float): The current relative specificity value.

        Returns:
            str: A random class from a list of filtered classes.
        """
        potential_classes = self.filter_classes(current_rel_specificity)

        return random.choice(potential_classes)

    def sample_class_constrained(self, current_rel_specificity, other_class):
        """
        Returns a compatible class based on the current relational specificity and other class.

        Args:
            self (object): The instance of the RelationGenerator.
            current_rel_specificity (float): The current relational specificity.
            other_class (str): The other class.

        Returns:
            str: A compatible class.
        """
        compatible_classes = []

        while not compatible_classes:
            potential_classes = self.filter_classes(current_rel_specificity)
            compatible_classes = list(set(potential_classes) - set(self.class2disjoints_extended.get(other_class, [])))

        return random.choice(compatible_classes)

    def filter_classes(self, current_rel_specificity):
        """
        Filters classes based on the current relational specificity.

        Args:
            self (object): The instance of the RelationGenerator.
            current_rel_specificity (float): The current relational specificity.

        Returns:
            list: A list of filtered classes.
        """
        if current_rel_specificity < self.relation_specificity:
            filtered_classes = [
                cl for layer, cl in self.layer2classes.items() if layer > int(self.relation_specificity)
            ]
            if random.random() < 0.1:  # add some noise
                filtered_classes = [
                    cl for layer, cl in self.layer2classes.items() if layer <= int(self.relation_specificity)
                ]
        else:
            filtered_classes = [
                cl for layer, cl in self.layer2classes.items() if layer <= int(self.relation_specificity)
            ]
            if random.random() < 0.1:  # add some noise
                filtered_classes = [
                    cl for layer, cl in self.layer2classes.items() if layer > int(self.relation_specificity)
                ]

        return list(itertools.chain.from_iterable(filtered_classes))

    def get_one_rel_compatibilities(self):
        """
        Gets all valid combinations of relation properties.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        file_path = pkg_resources.resource_filename("pygraft", "property_checks/combinations.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        compatibilities = [key for key, value in data.items() if value == "True"]
        self.one_rel_compatibilities = [op.split(",") for op in compatibilities]

    def get_inverseof_compatibilities(self):
        """
        Gets all valid combinations of inverse relations.

        Args:
            self (object): The instance of the RelationGenerator.
        
        Returns:
            None
        """
        self.compat_inverseof = {}
        file_path = pkg_resources.resource_filename("pygraft", "property_checks/compat_p1p2_inverseof.txt")

        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if "True" in line:
                    line = line.split(" ")
                    line[0] = line[0][:-1]
                    line = line[0].split("|")
                    v1 = frozenset(line[0].strip().split(","))
                    v2 = frozenset(line[1].strip().split(","))
                    if v1 not in self.compat_inverseof:
                        self.compat_inverseof[v1] = [v2]
                    else:
                        self.compat_inverseof[v1].append(v2)

    def update_rel2patterns(self, property):
        """
        Updates self.rel2patterns dictionary based on the given property.

        Args:
            self (object): The instance of the RelationGenerator.
            property (str): The property to add to the self.rel2patterns dictionary.

        Returns:
            None
        """
        property_mappings = {
            "owl:Reflexive": getattr(self, "reflexive_relations", set()),
            "owl:Irreflexive": getattr(self, "irreflexive_relations", set()),
            "owl:Symmetric": getattr(self, "symmetric_relations", set()),
            "owl:Asymmetric": getattr(self, "asymmetric_relations", set()),
            "owl:Transitive": getattr(self, "transitive_relations", set()),
        }

        if property in property_mappings:
            self.rel2patterns = {
                rel: property_set | {property} if rel in property_mappings[property] else property_set
                for rel, property_set in self.rel2patterns.items()
            }

        self.update_pattern2rels()

    def update_pattern2rels(self):
        """
        Updates self.pattern2rels dictionary.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        self.pattern2rels = defaultdict(set)
        _ = [self.pattern2rels[frozenset(value)].add(key) for key, value in self.rel2patterns.items()]

    def add_property(self, property):
        """
        Adds properties to relations.

        Args:
            self (object): The instance of the RelationGenerator.
            property (str): The property to add.

        Returns:
            None
        """
        # get all valid combinations featuring the desired property
        combinations_with_property = list(filter(lambda combi: property in combi, self.one_rel_compatibilities))
        # remove the desired property so that later on we ensure to sample relation s.t. adding a property is legit
        combinations_without_property = [
            list(filter(lambda item: item != property, combi)) for combi in combinations_with_property
        ]
        # get all relations having one of the valid combinations
        relation_pool = set().union(
            *[self.pattern2rels.get(frozenset(combi), set()) for combi in combinations_without_property]
        )

        if property == "owl:Functional":
            self.functional_relations = []
            potential_relations = [key for key, values in self.rel2patterns.items() if values == set()]
            while (
                len(self.functional_relations) < self.prop_functional_relations * self.num_relations
                and potential_relations
            ):
                new_functional_relation = potential_relations.pop()
                self.functional_relations.append(new_functional_relation)
                self.rel2patterns[new_functional_relation] = set(self.rel2patterns[new_functional_relation]) | {
                    "owl:Functional"
                }

        if property == "owl:InverseFunctional":
            self.inversefunctional_relations = []
            X = random.uniform(0.25, 0.75)
            potential_relations = [key for key, values in self.rel2patterns.items() if not values]
            while (
                len(self.inversefunctional_relations) < X * self.prop_inverse_functional_relations * self.num_relations
                and potential_relations
            ):
                new_inversefunctional_relation = potential_relations.pop()
                self.inversefunctional_relations.append(new_inversefunctional_relation)
                self.rel2patterns[new_inversefunctional_relation] = set(
                    self.rel2patterns[new_inversefunctional_relation]
                ) | {"owl:InverseFunctional"}

            potential_relations = [key for key, values in self.rel2patterns.items() if not values - {"owl:Functional"}]
            potential_relations = [r for r in potential_relations if r not in self.inversefunctional_relations]
            while (
                len(self.inversefunctional_relations) < self.prop_inverse_functional_relations * self.num_relations
                and potential_relations
            ):
                new_inversefunctional_relation = potential_relations.pop()
                self.inversefunctional_relations.append(new_inversefunctional_relation)
                self.rel2patterns[new_inversefunctional_relation] = set(
                    self.rel2patterns[new_inversefunctional_relation]
                ) | {"owl:InverseFunctional"}

        if property == "rdfs:subPropertyOf":
            self.prop2superprop = {}
            self.subproperties = []
            rels = self.relations[:]
            for r1 in rels:
                for r2 in rels:
                    if (
                        r1 != r2
                        and r1 not in self.prop2superprop
                        and r2 not in self.prop2superprop
                        and self.rel2inverse.get(r1) != r2
                        and self.rel2inverse.get(r2) != r1
                        and self.rel2patterns[r1] == self.rel2patterns[r2]
                    ):
                        if (
                            r1 not in self.rel2dom
                            and r1 not in self.rel2range
                            and r2 not in self.rel2dom
                            and r1 not in self.rel2range
                        ):
                            self.prop2superprop[r1] = r2
                            self.subproperties.append(r1)
                            break
                        if r1 in self.rel2dom and r1 in self.rel2range and r2 in self.rel2dom and r1 in self.rel2range:
                            # 1
                            if self.rel2dom.get(r1) == self.rel2dom.get(r2) and self.rel2range.get(
                                r1
                            ) == self.rel2range.get(r2):
                                self.prop2superprop[r1] = r2
                                self.subproperties.append(r1)
                                break
                            # 2
                            elif (
                                self.rel2dom.get(r1) == self.rel2dom.get(r2)
                                and self.rel2range.get(r2)
                                in self.class_info["transitive_class2superclasses"][self.rel2range.get(r1)]
                            ):
                                self.prop2superprop[r1] = r2
                                self.subproperties.append(r1)
                                break
                            # 3
                            elif (
                                self.rel2range.get(r1) == self.rel2range.get(r2)
                                and self.rel2dom.get(r2)
                                in self.class_info["transitive_class2superclasses"][self.rel2dom.get(r1)]
                            ):
                                self.prop2superprop[r1] = r2
                                self.subproperties.append(r1)
                                break
                            # 4
                            elif (
                                self.rel2dom.get(r2)
                                in self.class_info["transitive_class2superclasses"][self.rel2dom.get(r1)]
                                and self.rel2range.get(r2)
                                in self.class_info["transitive_class2superclasses"][self.rel2range.get(r1)]
                            ):
                                self.prop2superprop[r1] = r2
                                self.subproperties.append(r1)
                                break

                if 2 * len(self.prop2superprop) >= self.prop_subproperties * self.num_relations:
                    return

        if property == "owl:Symmetric":
            sample_size = int(len(self.relations) * self.prop_symmetric_relations)
            if sample_size > len(relation_pool):
                sample_size = len(relation_pool)
            self.symmetric_relations = random.sample(list(relation_pool), k=sample_size)

        if property == "owl:Asymmetric":
            sample_size = int(len(self.relations) * self.prop_asymmetric_relations)
            if sample_size > len(relation_pool):
                sample_size = len(relation_pool)
            self.asymmetric_relations = random.sample(list(relation_pool), k=sample_size)

        if property == "owl:Transitive":
            sample_size = int(len(self.relations) * self.prop_transitive_relations)
            if sample_size > len(relation_pool):
                sample_size = len(relation_pool)
            self.transitive_relations = random.sample(list(relation_pool), k=sample_size)

        # update rel2patterns
        self.update_rel2patterns(property)

    def add_inverseof(self):
        """
        Determines and adds inverse relations based on observed patterns and compatibility.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        observed_patterns = [frozenset(op) for op in self.rel2patterns.values()]
        running_inverseof_prop = 0.0
        attempt = 0
        warning_msg = 0

        # first with relations without pattern
        unpatterned_relations = [r for r in self.relations if not self.rel2patterns[r]]
        unpatterned_relations = (
            unpatterned_relations[:-1] if len(unpatterned_relations) % 2 == 1 else unpatterned_relations
        )

        while running_inverseof_prop < self.prop_inverse_relations and len(unpatterned_relations) >= 2:
            first_rel = unpatterned_relations.pop()
            second_rel = unpatterned_relations.pop()
            self.pair_inverseof(first_rel, second_rel)
            running_inverseof_prop = self.calculate_inverseof()

        while running_inverseof_prop < self.prop_inverse_relations:
            attempt += 1
            try:
                first_pattern = random.choice(observed_patterns)
                compatible_patterns = set(self.compat_inverseof[frozenset(first_pattern)])
                possible_pattern = set(observed_patterns).intersection(compatible_patterns)
                second_pattern = random.choice(list(possible_pattern))
                first_rel = random.choice(list(self.pattern2rels[frozenset(first_pattern)]))
                second_rel = random.choice(list(self.pattern2rels[frozenset(second_pattern)]))

                if (
                    first_rel != second_rel
                    and first_rel not in self.rel2inverse
                    and second_rel not in self.rel2inverse
                    and "owl:Reflexive" not in self.rel2patterns[first_rel]
                    and "owl:Reflexive" not in self.rel2patterns[second_rel]
                    and "owl:Irreflexive" not in self.rel2patterns[first_rel]
                    and "owl:Irreflexive" not in self.rel2patterns[second_rel]
                    and "owl:Symmetric" not in self.rel2patterns[first_rel]
                    and "owl:Symmetric" not in self.rel2patterns[second_rel]
                    and not (
                        "owl:Asymmetric" in self.rel2patterns[first_rel]
                        and "owl:Asymmetric" in self.rel2patterns[second_rel]
                    )
                ):
                    self.pair_inverseof(first_rel, second_rel)
                    running_inverseof_prop = self.calculate_inverseof()
                    attempt = 0
                else:
                    attempt += 1
                    if attempt > 1000:
                        self.prop_inverse_relations -= 0.005
                        attempt = 0
                        warning_msg = 1
            except:
                continue

        if warning_msg:
            print("Proportion of inverse relations reduced due to incompatibilities with other properties.")

    def pair_inverseof(self, rel, inv_rel):
        """
        Pairs relations as inverse relations.

        Args:
            self (object): The instance of the RelationGenerator.
            rel (str): The first relation.
            inv_rel (str): The second relation.

        Returns:
            None
        """
        self.inverseof_relations.append(rel)
        self.inverseof_relations.append(inv_rel)
        self.rel2inverse[rel] = inv_rel
        self.rel2inverse[inv_rel] = rel

    def calculate_inverseof(self):
        """
        Calculates the proportion of inverse relations.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            float: The proportion of inverse relations.
        """
        return len(self.inverseof_relations) / len(self.relations)

    def print_schema(self):
        """
        Prints the relation schema and
        displays various metrics and values related to the relations.

        Args:
            self (object): The instance of the RelationGenerator.

        Returns:
            None
        """
        print("\n")

        table = [
            ["Number of Relations", len(self.relations), self.num_relations],
            [
                "SubProperty Proportion",
                round(2 * len(self.prop2superprop) / len(self.relations), 2),
                self.prop_subproperties,
            ],
            [
                "Reflexive Relations",
                round(len(self.reflexive_relations) / len(self.relations), 2),
                self.prop_reflexive_relations,
            ],
            [
                "Irreflexive Relations",
                round(len(self.irreflexive_relations) / len(self.relations), 2),
                self.prop_irreflexive_relations,
            ],
            [
                "Functional Relations",
                round(len(self.functional_relations) / len(self.relations), 2),
                self.prop_functional_relations,
            ],
            [
                "InverseFunctional Relations",
                round(len(self.inversefunctional_relations) / len(self.relations), 2),
                self.prop_inverse_functional_relations,
            ],
            [
                "Symmetric Relations",
                round(len(self.symmetric_relations) / len(self.relations), 2),
                self.prop_symmetric_relations,
            ],
            [
                "Asymmetric Relations",
                round(len(self.asymmetric_relations) / len(self.relations), 2),
                self.prop_asymmetric_relations,
            ],
            [
                "Transitive Relations",
                round(len(self.transitive_relations) / len(self.relations), 2),
                self.prop_transitive_relations,
            ],
            [
                "InverseOf Relations",
                round(len(self.inverseof_relations) / len(self.relations), 2),
                round(self.prop_inverse_relations, 2),
            ],
            ["Profiled Relations", round(self.current_profile_ratio, 2), self.prop_profiled_relations],
            ["Relation Specificity", round(self.calculate_relation_specificity(), 2), self.relation_specificity],
        ]

        headers = ["Relation Metric", "Value", "Specified Value"]
        table_str = tabulate(table, headers, tablefmt="pretty")
        print(table_str)
        print("\n")
