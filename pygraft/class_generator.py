import random
import copy
import numpy as np
from collections import defaultdict
from pygraft.utils_schema import *
from tabulate import tabulate


class ClassGenerator:
    def __init__(self, **kwargs):
        self.init_params(**kwargs)
        self.init_class_structures()

    def init_params(self, **kwargs):
        """
        Initializes the parameters for the class generator.

        Args:
            self (object): The instance of the ClassGenerator.
            kwargs (dict): The keyword arguments.

        Returns:
            None
        """
        self.num_classes = kwargs.get("num_classes")
        self.max_hierarchy_depth = kwargs.get("max_hierarchy_depth")
        self.avg_class_depth = kwargs.get("avg_class_depth")
        self.class_inheritance_ratio = kwargs.get("class_inheritance_ratio")
        self.avg_disjointness = kwargs.get("avg_disjointness")
        self.verbose = kwargs.get("verbose")

    def init_class_structures(self):
        """
        Initializes the class structures for the class generator.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:    
            None
        """
        self.classes = None
        self.class2superclass_direct = {}
        self.class2superclasses_transitive = defaultdict(list)
        self.class2subclasses_direct = defaultdict(list)
        self.class2subclasses_transitive = defaultdict(list)
        self.layer2classes = defaultdict(list)

    def generate_class_schema(self):
        """
        Generates a class schema based on the given parameters.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            class_info (dict): A dictionary containing various information about the class.
        """
        self.generate_class_hierarchy()
        self.generate_class_disjointness()

        if self.verbose:
            self.print_schema()

        class_info = self.assemble_class_info()

        return class_info

    def assemble_class_info(self):
        """
        Assembles and returns information about the current class schema.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            class_info (dict): A dictionary containing various information about the class.
        """
        class_info = {
            "num_classes": len(self.classes),
            "classes": self.classes,
            "hierarchy_depth": get_max_depth(self.layer2classes),
            "avg_class_depth": round(calculate_average_depth(self.layer2classes), 2),
            "class_inheritance_ratio": round(
                calculate_inheritance_ratio(self.class2superclass_direct, self.class2subclasses_direct), 2
            ),
            "direct_class2subclasses": self.class2subclasses_direct,
            "direct_class2superclass": self.class2superclass_direct,
            "transitive_class2subclasses": self.class2subclasses_transitive,
            "transitive_class2superclasses": self.class2superclasses_transitive,
            "avg_class_disjointness": round(calculate_class_disjointness(self.disjointwith, len(self.classes)), 2),
            "class2disjoints": self.disjointwith,
            "class2disjoints_symmetric": self.mutual_disjointness,
            "class2disjoints_extended": {c: list(set(classes)) for c, classes in self.disjointwith_extended.items()},
            "layer2classes": {int(k): v for k, v in self.layer2classes.items()},
            "class2layer": generate_class2layer(self.layer2classes),
        }

        return class_info

    def generate_classes(self):
        """
        Generates the classes for the given self instance based on the
        given number of classes.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            None
        """
        self.classes = [f"C{i}" for i in range(1, self.num_classes + 1)]

    def generate_class_hierarchy(self):
        """
        Generate the class hierarchy for the given self instance.
        This function creates a hierarchical structure of classes based on the
        existing classes in the self instance. It assigns each class to a layer
        and establishes the parent-child relationships between them.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            None
        """
        self.generate_classes()

        unconnected_classes = copy.deepcopy(self.classes)

        c = unconnected_classes.pop()
        self.link_child2parent(c, "owl:Thing", layer=1)

        for layer in range(1, self.max_hierarchy_depth):
            c2 = unconnected_classes.pop()
            self.link_child2parent(c2, c, layer=layer + 1)
            c = c2

        current_avg_depth = calculate_average_depth(self.layer2classes)
        current_inheritance_ratio = calculate_inheritance_ratio(
            self.class2superclass_direct, self.class2subclasses_direct
        )

        stochastic_noise_until = int(len(unconnected_classes) * 0.5)

        while unconnected_classes:
            c = unconnected_classes.pop()

            if (
                random.random() < 0.35
                and len(unconnected_classes) >= stochastic_noise_until
                and self.max_hierarchy_depth > 3
            ):
                self.noisy_placing(c, current_avg_depth, current_inheritance_ratio)
            else:
                self.smart_placing(c, current_avg_depth, current_inheritance_ratio)

            current_avg_depth = calculate_average_depth(self.layer2classes)
            current_inheritance_ratio = calculate_inheritance_ratio(
                self.class2superclass_direct, self.class2subclasses_direct
            )

    def smart_placing(self, c, current_avg_depth, current_inheritance_ratio):
        """
        Determines the appropriate action to take based on the current average depth 
        and current inheritance ratio.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): A given class.
            current_avg_depth (float): The current average depth.
            current_inheritance_ratio (float): The current inheritance ratio.

        Returns:
            None
        """

        if current_avg_depth <= self.avg_class_depth and current_inheritance_ratio <= self.class_inheritance_ratio:
            self.create_deep_leaf_realistic(c)
        elif current_avg_depth <= self.avg_class_depth and current_inheritance_ratio > self.class_inheritance_ratio:
            self.create_deep_child_realistic(c)
        elif current_avg_depth > self.avg_class_depth and current_inheritance_ratio <= self.class_inheritance_ratio:
            self.create_shallow_leaf(c)
        elif current_avg_depth > self.avg_class_depth and current_inheritance_ratio > self.class_inheritance_ratio:
            self.create_shallow_leaf_root(c)

    def noisy_placing(self, c, current_avg_depth, current_inheritance_ratio):
        """
        Adds noise to the class hierarchy tree to create more diverse shapes.
        This function adds randomness to the placement of classes in the hierarchy tree.
        Without this optional noise, trees tend to be vertical with only a few parents having most children.
        By putting more weight on the intermediate layers, which tend to be underpopulated otherwise,
        the hierarchy becomes more realistic.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be placed in the hierarchy tree.
            current_avg_depth (float): The current average depth of the hierarchy tree.
            current_inheritance_ratio (float): The current inheritance ratio of the hierarchy tree.

        Returns:
            None
        """

        focus_layers = [key - 1 for key, value in self.layer2classes.items() if value]
        # the parent will not be in 1st or penultimate layer:
        focus_layers = [l for l in focus_layers if l not in [0, 1, self.max_hierarchy_depth - 1]]

        if focus_layers:
            layer = random.choice(focus_layers)
            parent = random.choice(self.layer2classes[layer])
            self.link_child2parent(c, parent, layer=layer + 1)
        else:
            self.smart_placing(c, current_avg_depth, current_inheritance_ratio)

    def create_deep_leaf_realistic(self, c):
        """
        Create a child to an already existing parent which is deep in the class hierarchy.

        => |S| += 1; |C| += 1; |L| += 1
        => Inheritance ratio increases.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be placed.

        Returns:
            None
        """
        deep_layers = [key - 1 for key, value in self.layer2classes.items() if value and key >= self.avg_class_depth]
        layer = random.choice(deep_layers)

        while True:
            current_parents = [c for c in self.layer2classes[layer] if c in self.class2subclasses_direct.keys()]

            if current_parents:
                parent = random.choice(current_parents)
                self.link_child2parent(c, parent, layer=layer + 1)
                break
            else:
                layer -= 1

    def create_deep_leaf_deterministic(self, c):
        """
        Creates a child to an already existing parent which is deep in the class hierarchy.

        => |S| += 1; |C| += 1; |L| += 1
        => Inheritance ratio increases.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be placed.

        Returns:
            None
        """
        found = False
        layer = max((key for key, value in self.layer2classes.items() if value), default=None) - 1

        while not found:
            current_parents = [c for c in self.layer2classes[layer] if c in self.class2subclasses_direct.keys()]

            if current_parents:
                found = True
                parent = random.choice(current_parents)
                self.link_child2parent(c, parent, layer=layer + 1)
            else:
                layer -= 1

    def create_deep_child_realistic(self, c):
        """
        Creates a child to a leaf which is deep in the class hierarchy.

        => |S| += 1; |C| += 1; |L| = |L| (unchanged)
        => Inheritance ratio decreases.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be placed.

        Returns:
            None
        """
        found = False
        deep_layers = [key - 1 for key, value in self.layer2classes.items() if value and key >= self.avg_class_depth]
        layer = random.choice(deep_layers)

        while not found:
            current_leaves = [c for c in self.layer2classes[layer] if c not in self.class2subclasses_direct.keys()]

            if current_leaves:
                found = True
                parent = random.choice(current_leaves)
                self.link_child2parent(c, parent, layer=layer + 1)
            else:
                layer -= 1

    def create_deep_child_deterministic(self, c):
        """
        Creates a child to a leaf which is deep in the class hierarchy.

        => |S| += 1; |C| += 1; |L| = |L| (unchanged)
        => Inheritance ratio decreases.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be placed.

        Returns:
            None
        """
        found = False
        layer = max((key for key, value in self.layer2classes.items() if value), default=None) - 1

        while not found:
            current_leaves = [c for c in self.layer2classes[layer] if c not in self.class2subclasses_direct.keys()]

            if current_leaves:
                found = True
                parent = random.choice(current_leaves)
                self.link_child2parent(c, parent, layer=layer + 1)
            else:
                layer -= 1

    def create_shallow_leaf(self, c):
        """
        Creates a shallow leaf by adding a new class to the class hierarchy.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The class to be added as a shallow leaf.

        Returns:
            None
        """
        layer = 1
        parent = random.choice(self.layer2classes[layer])
        self.link_child2parent(c, parent, layer=layer + 1)

    def create_shallow_leaf_root(self, c):
        """
        Creates a leaf which is placed just under the root of the class hierarchy.

        Args:
            self (object): The instance of the ClassGenerator.
            c (str): The name of the class.

        Returns:
            None
        """
        self.link_child2parent(c, "owl:Thing", layer=1)

    def generate_class_disjointness(self):
        """
        Generates class disjointness by randomly selecting two classes and making them incompatible.
        Updates the class mappings and extend the incompatibilities to subclasses.
        Calculates the current class disjointness and stops when average disjointness threshold is reached.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            None
        """
        current_class_disjointness = 0.0
        self.class2superclasses_transitive, self.class2subclasses_transitive = extend_class_mappings(
            self.class2superclass_direct
        )
        self.disjointwith, self.disjointwith_extended, self.mutual_disjointness = {}, {}, set()

        while current_class_disjointness < self.avg_disjointness:
            found = False
            while not found:
                # pick one class A randomly
                A = random.choice(self.classes)
                # pick another class B randomly that is neither a transitive parent nor child of A
                B = random.choice(self.classes)
                while (
                    B == A
                    or (A in self.class2superclasses_transitive and B in self.class2superclasses_transitive[A])
                    or (A in self.class2subclasses_transitive and B in self.class2subclasses_transitive[A])
                ):
                    B = random.choice(self.classes)
                found = True

            # make A and B incompatible
            self.disjointwith.setdefault(A, []).append(B)
            self.disjointwith.setdefault(B, []).append(A)
            self.disjointwith_extended.setdefault(A, []).append(B)
            self.disjointwith_extended.setdefault(B, []).append(A)
            mutual_disj_key = f"{A}-{B}" if int(A[1:]) < int(B[1:]) else f"{B}-{A}"
            self.mutual_disjointness.add(mutual_disj_key)
            # iterate through subclasses of A and B, and make them incompatible
            self.extend_incompatibilities(A, B)
            # update current class disjointness
            current_class_disjointness = calculate_class_disjointness(self.disjointwith, self.num_classes)

    def extend_incompatibilities(self, class_A, class_B):
        """
        Extends the incompatibilities between two classes.

        Args:
            self (object): The instance of the ClassGenerator.
            class_A (str): The first class.
            class_B (str): The second class.

        Returns:
            None
        """
        children_A = self.class2subclasses_transitive.get(class_A, [])
        children_B = self.class2subclasses_transitive.get(class_B, [])

        # Iterate over the transitive children of class A
        for child_A in children_A:
            # Iterate over the transitive children of class B
            for child_B in children_B:
                self.disjointwith_extended.setdefault(child_A, []).append(child_B)
                self.disjointwith_extended.setdefault(child_B, []).append(child_A)
                mutual_disj_key = (
                    f"{child_A}-{child_B}" if int(child_A[1:]) < int(child_B[1:]) else f"{child_B}-{child_A}"
                )
                self.mutual_disjointness.add(mutual_disj_key)

        # Handle the case where class A has no children
        if not children_A:
            for child_B in children_B:
                self.disjointwith_extended.setdefault(class_A, []).append(child_B)
                self.disjointwith_extended.setdefault(child_B, []).append(class_A)
                mutual_disj_key = (
                    f"{class_A}-{child_B}" if int(class_A[1:]) < int(child_B[1:]) else f"{child_B}-{class_A}"
                )
                self.mutual_disjointness.add(mutual_disj_key)

        # Handle the case where class B has no children
        if not children_B:
            for child_A in children_A:
                self.disjointwith_extended.setdefault(child_A, []).append(class_B)
                self.disjointwith_extended.setdefault(class_B, []).append(child_A)
                mutual_disj_key = (
                    f"{class_B}-{child_A}" if int(class_B[1:]) < int(child_A[1:]) else f"{child_A}-{class_B}"
                )
                self.mutual_disjointness.add(mutual_disj_key)

    def link_child2parent(self, child, parent, layer):
        self.class2subclasses_direct[parent] = [child]
        self.class2superclass_direct[child] = parent
        self.layer2classes[layer].append(child)

    def print_schema(self):
        """
        Prints the generated class schema.

        Args:
            self (object): The instance of the ClassGenerator.

        Returns:
            None
        """
        print("Ontology Generated.")
        print("===================")
        print("Ontology Parameters:")
        print("===================")
        print("\n")

        table = [
            ["Number of Classes", len(self.classes), self.num_classes],
            ["Maximum Hierarchy Depth", get_max_depth(self.layer2classes), self.max_hierarchy_depth],
            ["Average Class Depth", round(calculate_average_depth(self.layer2classes), 2), self.avg_class_depth],
            [
                "Class Inheritance Ratio",
                round(calculate_inheritance_ratio(self.class2superclass_direct, self.class2subclasses_direct), 2),
                self.class_inheritance_ratio,
            ],
            [
                "Average Disjointness",
                round(calculate_class_disjointness(self.disjointwith, len(self.classes)), 2),
                self.avg_disjointness,
            ],
        ]

        headers = ["Class Metric", "Value", "Specified Value"]
        table_str = tabulate(table, headers, tablefmt="pretty")
        print(table_str)
