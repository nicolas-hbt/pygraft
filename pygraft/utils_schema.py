from collections import defaultdict

def non_trivial_children(class2superclass_direct):
    return [c for c in class2superclass_direct.keys() if class2superclass_direct[c] != "owl:Thing"]

# same as above
def get_subclassof_count(class2layer):
    return len([key for key, value in class2layer.items() if value > 1])

def get_leaves(class2superclass_direct, class2subclasses_direct):
    return set(class2superclass_direct.keys()) - set(class2subclasses_direct.keys())

def get_max_depth(layer2classes):
    return max((key for key, value in layer2classes.items() if value), default=None)

def calculate_inheritance_ratio(class2superclass_direct, class2subclasses_direct):
    n_classes = len(class2superclass_direct.keys()) 
    n_leaves = len(get_leaves(class2superclass_direct, class2subclasses_direct))
    n_non_trivial_children = len(non_trivial_children(class2superclass_direct))

    return n_non_trivial_children / (n_classes - n_leaves)

def calculate_average_depth(layer2classes):
    denominator = sum(map(len, layer2classes.values()))
    numerator = 0.0

    for key, value in layer2classes.items():
        numerator += key * len(value)

    return numerator / denominator
    
def calculate_class_disjointness(class2disjoint, num_classes):
    return len(class2disjoint) / (2 * num_classes)

def get_transitive_subclasses(transitive_class2superclasses):
    class2subclasses = defaultdict(list)

    for subclass, superclasses in transitive_class2superclasses.items():
        for superclass in superclasses:
            class2subclasses[superclass].append(subclass)

    return dict(class2subclasses)

def get_all_superclasses(class_name, direct_class2superclass):
    superclasses = []

    if class_name in direct_class2superclass:
        superclass = direct_class2superclass[class_name]
        superclasses.append(superclass)
        superclasses.extend(get_all_superclasses(superclass, direct_class2superclass))

    return superclasses

def get_all_subclasses(transitive_class2superclass):
    class2subclasses = defaultdict(list)

    for subclass, superclasses in transitive_class2superclass.items():
        for superclass in superclasses:
            class2subclasses[superclass].append(subclass)

    return dict(class2subclasses)

def extend_class_mappings(direct_class2superclass):
    transitive_class2superclass = {}
    transitive_class2subclasses = {}

    for class_name in direct_class2superclass:
        # Extend superclasses recursively
        transitive_superclasses = get_all_superclasses(class_name, direct_class2superclass)
        transitive_class2superclass[class_name] = transitive_superclasses

    transitive_class2subclasses = get_all_subclasses(transitive_class2superclass)

    return transitive_class2superclass, transitive_class2subclasses

def generate_class2layer(layer2classes):
    class2layer = {}

    for layer, classes in layer2classes.items():
        for c in classes:
            class2layer[c] = layer

    return class2layer