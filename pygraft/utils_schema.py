from collections import defaultdict


def non_trivial_children(class2superclass_direct):
    """
    Returns a list of classes that have at least one non-trivial parent.
    
    Args:
        class2superclass_direct (dict): A dictionary mapping classes to their direct superclasses.
        
    Returns:
        list: A list of classes that have at least one non-trivial parent.
    """
    return [c for c in class2superclass_direct.keys() if class2superclass_direct[c] != "owl:Thing"]


def get_subclassof_count(class2layer):
    """
    Returns the number of classes that have at least one subclass.
    
    Args:
        class2layer (dict): A dictionary mapping classes to their layers.
        
    Returns:
        int: The number of classes that have at least one non-trivial parent.
    """
    return len([key for key, value in class2layer.items() if value > 1])


def get_leaves(class2superclass_direct, class2subclasses_direct):
    """
    Returns a list of classes that have no subclasses, i.e. leaves.

    Args:
        class2superclass_direct (dict): A dictionary mapping classes to their direct superclasses.
        class2subclasses_direct (dict): A dictionary mapping classes to their direct subclasses.

    Returns:
        list: A list of classes that have no subclasses.
    """
    return set(class2superclass_direct.keys()) - set(class2subclasses_direct.keys())


def get_max_depth(layer2classes):
    """
    Returns the maximum depth of the schema.

    Args:
        layer2classes (dict): A dictionary mapping layers to classes.

    Returns:
        int: The maximum depth of the schema.
    """
    return max((key for key, value in layer2classes.items() if value), default=None)


def calculate_inheritance_ratio(class2superclass_direct, class2subclasses_direct):
    """
    Calculates the inheritance ratio of the schema.

    Args:
        class2superclass_direct (dict): A dictionary mapping classes to their direct superclasses.
        class2subclasses_direct (dict): A dictionary mapping classes to their direct subclasses.

    Returns:
        float: The inheritance ratio of the schema.
    """
    n_classes = len(class2superclass_direct.keys())
    n_leaves = len(get_leaves(class2superclass_direct, class2subclasses_direct))
    n_non_trivial_children = len(non_trivial_children(class2superclass_direct))

    return n_non_trivial_children / (n_classes - n_leaves)


def calculate_average_depth(layer2classes):
    """
    Calculates the average depth of the schema.

    Args:
        layer2classes (dict): A dictionary mapping layers to classes.

    Returns:
        float: The average depth of the schema.
    """
    denominator = sum(map(len, layer2classes.values()))
    numerator = 0.0

    for key, value in layer2classes.items():
        numerator += key * len(value)

    return numerator / denominator


def calculate_class_disjointness(class2disjoint, num_classes):
    """
    Calculates the class disjointness of the schema.

    Args:
        class2disjoint (dict): A dictionary mapping classes to their disjoint classes.
        num_classes (int): The number of classes.

    Returns:
        float: The class disjointness of the schema.
    """
    return len(class2disjoint) / (2 * num_classes)


def get_all_superclasses(class_name, direct_class2superclass):
    """
    Returns a list of all superclasses of a given class.
    
    Args:
        class_name (str): The name of the class.
        direct_class2superclass (dict): A dictionary mapping classes to their direct superclasses.
        
    Returns:
        list: A list of all superclasses of the given class.
    """
    superclasses = []

    if class_name in direct_class2superclass:
        superclass = direct_class2superclass[class_name]
        superclasses.append(superclass)
        superclasses.extend(get_all_superclasses(superclass, direct_class2superclass))

    return superclasses


def get_all_subclasses(transitive_class2superclass):
    """
    Returns a dictionary mapping classes to their transitive subclasses.

    Args:
        transitive_class2superclass (dict): A dictionary mapping classes to their transitive superclasses.

    Returns:
        dict: A dictionary mapping classes to their subclasses.
    """
    class2subclasses = defaultdict(list)

    for subclass, superclasses in transitive_class2superclass.items():
        for superclass in superclasses:
            class2subclasses[superclass].append(subclass)

    return dict(class2subclasses)


def extend_class_mappings(direct_class2superclass):
    """
    Extends the class mappings to include transitive superclasses and subclasses.

    Args:
        direct_class2superclass (dict): A dictionary mapping classes to their direct superclasses.

    Returns:
        tuple: A tuple containing the extended class mappings.
    """
    transitive_class2superclass = {}
    transitive_class2subclasses = {}

    for class_name in direct_class2superclass:
        # Extend superclasses recursively
        transitive_superclasses = get_all_superclasses(class_name, direct_class2superclass)
        transitive_class2superclass[class_name] = transitive_superclasses

    transitive_class2subclasses = get_all_subclasses(transitive_class2superclass)

    return transitive_class2superclass, transitive_class2subclasses


def generate_class2layer(layer2classes):
    """
    Generates a dictionary mapping classes to their layers.

    Args:
        layer2classes (dict): A dictionary mapping layers to classes.

    Returns:
        dict: A dictionary mapping classes to their layers.
    """
    class2layer = {}

    for layer, classes in layer2classes.items():
        for c in classes:
            class2layer[c] = layer

    return class2layer
