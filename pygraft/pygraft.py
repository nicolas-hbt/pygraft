from .schema_constructor import SchemaBuilder
from .utils import (
    get_most_recent_subfolder,
    load_config,
    initialize_folder,
    check_schema_arguments,
    check_kg_arguments,
    print_ascii_header,
    load_json_template,
    load_yaml_template,
)
from .class_generator import ClassGenerator
from .relation_generator import RelationGenerator
from .kg_generator import InstanceGenerator


def create_template(extension="yml"):
    """
    Creates a template file for the user to fill in.

    Args:
        extension (str, optional): File extension of the template file. Defaults to "yml".

    Raises:
        ValueError: If the extension is not one of the following: json, yaml, yml

    Returns:
        None
    """
    if extension == "json":
        load_json_template()
    elif extension in {"yaml", "yml"}:
        load_yaml_template()
    else:
        raise ValueError(
            f"Unknown extension file format: {extension}. Please enter one of the following: json, yaml, yml"
        )


def create_json_template():
    """
    Creates a json template file for the user to fill in.

    Args:
        None
    
    Returns:
        None
    """
    load_json_template()


def create_yaml_template():
    """
    Creates a yaml template file for the user to fill in.

    Args:
        None

    Returns:
        None
    """
    load_yaml_template()


def generate_schema(path):
    """
    Generates a schema based on the user's configuration file.
    
    Args:
        path (str): Path to the user's configuration file.
        
    Returns:
        None
    """
    config = load_config(path)
    check_schema_arguments(config)
    config["schema_name"] = initialize_folder(config["schema_name"])

    print_ascii_header()

    class_generator = ClassGenerator(
        num_classes=config["num_classes"],
        max_hierarchy_depth=config["max_hierarchy_depth"],
        avg_class_depth=config["avg_class_depth"],
        class_inheritance_ratio=config["class_inheritance_ratio"],
        avg_disjointness=config["avg_disjointness"],
        verbose=config["verbose"],
    )
    class_info = class_generator.generate_class_schema()

    relation_generator = RelationGenerator(
        class_info=class_info,
        num_relations=config["num_relations"],
        relation_specificity=config["relation_specificity"],
        prop_profiled_relations=config["prop_profiled_relations"],
        profile_side=config["profile_side"],
        prop_symmetric_relations=config["prop_symmetric_relations"],
        prop_inverse_relations=config["prop_inverse_relations"],
        prop_functional_relations=config["prop_functional_relations"],
        prop_transitive_relations=config["prop_transitive_relations"],
        prop_subproperties=config["prop_subproperties"],
        prop_reflexive_relations=config["prop_reflexive_relations"],
        prop_irreflexive_relations=config["prop_irreflexive_relations"],
        prop_asymmetric_relations=config["prop_asymmetric_relations"],
        prop_inverse_functional_relations=config["prop_inverse_functional_relations"],
        verbose=config["verbose"],
    )
    relation_info = relation_generator.generate_relation_schema()

    schema_builder = SchemaBuilder(class_info, relation_info, config["schema_name"], config["format"])
    schema_builder.building_pipeline()


def generate_kg(path):
    """
    Generates a knowledge graph based on the user's configuration file.

    Args:
        path (str): Path to the user's configuration file.

    Returns:
        None
    """
    config = load_config(path)
    check_kg_arguments(config)
    if config["schema_name"] is None:
        most_recent_subfolder_name = get_most_recent_subfolder("output")
        config["schema_name"] = most_recent_subfolder_name

    print_ascii_header()

    instance_generator = InstanceGenerator(
        schema=config["schema_name"],
        num_entities=config["num_entities"],
        num_triples=config["num_triples"],
        relation_balance_ratio=config["relation_balance_ratio"],
        fast_gen=config["fast_gen"],
        oversample=config["oversample"],
        prop_untyped_entities=config["prop_untyped_entities"],
        avg_depth_specific_class=config["avg_depth_specific_class"],
        multityping=config["multityping"],
        avg_multityping=config["avg_multityping"],
        format=config["format"],
    )
    instance_generator.generate_kg()


def generate(path):
    """
    Generates a schema and knowledge graph based on the user's configuration file.

    Args:
        path (str): Path to the user's configuration file.
    
    Returns:
        None
    """
    config = load_config(path)
    check_schema_arguments(config)
    check_kg_arguments(config)
    config["schema_name"] = initialize_folder(config["schema_name"])

    print_ascii_header()

    class_generator = ClassGenerator(
        num_classes=config["num_classes"],
        max_hierarchy_depth=config["max_hierarchy_depth"],
        avg_class_depth=config["avg_class_depth"],
        class_inheritance_ratio=config["class_inheritance_ratio"],
        avg_disjointness=config["avg_disjointness"],
        verbose=config["verbose"],
    )
    class_info = class_generator.generate_class_schema()

    relation_generator = RelationGenerator(
        class_info=class_info,
        num_relations=config["num_relations"],
        relation_specificity=config["relation_specificity"],
        prop_profiled_relations=config["prop_profiled_relations"],
        profile_side=config["profile_side"],
        prop_symmetric_relations=config["prop_symmetric_relations"],
        prop_inverse_relations=config["prop_inverse_relations"],
        prop_functional_relations=config["prop_functional_relations"],
        prop_transitive_relations=config["prop_transitive_relations"],
        prop_subproperties=config["prop_subproperties"],
        prop_reflexive_relations=config["prop_reflexive_relations"],
        prop_irreflexive_relations=config["prop_irreflexive_relations"],
        prop_asymmetric_relations=config["prop_asymmetric_relations"],
        prop_inverse_functional_relations=config["prop_inverse_functional_relations"],
        verbose=config["verbose"],
    )
    relation_info = relation_generator.generate_relation_schema()

    schema_builder = SchemaBuilder(class_info, relation_info, config["schema_name"], config["format"])
    schema_builder.building_pipeline()

    instance_generator = InstanceGenerator(
        schema=config["schema_name"],
        num_entities=config["num_entities"],
        num_triples=config["num_triples"],
        relation_balance_ratio=config["relation_balance_ratio"],
        fast_gen=config["fast_gen"],
        oversample=config["oversample"],
        prop_untyped_entities=config["prop_untyped_entities"],
        avg_depth_specific_class=config["avg_depth_specific_class"],
        multityping=config["multityping"],
        avg_multityping=config["avg_multityping"],
        format=config["format"],
    )
    instance_generator.generate_kg()
