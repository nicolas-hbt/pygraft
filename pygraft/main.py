import argparse
import os
from pygraft import create_json_template, create_yaml_template, generate_schema, generate_kg, generate


def parse_arguments():
    parser = argparse.ArgumentParser(description="================== Schema & KG Generator ==================")
    parser.add_argument(
        "-t",
        "--template",
        action="store_true",
        default=None,
        help="Create a config template in the current working directory.",
    )
    parser.add_argument(
        "-e", "--extension", type=str, default=None, help="Config file extension. Options: json | yaml | yml"
    )
    parser.add_argument(
        "-jt",
        "--json_template",
        action="store_true",
        default=None,
        help="Create a json config template in the current working directory.",
    )
    parser.add_argument(
        "-yt",
        "--yaml_template",
        action="store_true",
        default=None,
        help="Create a yml config template in the current working directory.",
    )
    parser.add_argument("-conf", "--config", type=str, default=None, help="Load a given config file.")
    parser.add_argument(
        "-g",
        "--gen",
        type=str,
        default=None,
        help="Which function to call. Options: generate_schema | generate_kg | generate",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    if args.template:
        if args.extension == "json":
            create_json_template()
        else:
            create_yaml_template()

    if args.json_template:
        create_json_template()

    if args.yaml_template:
        create_yaml_template()

    if args.config:
        _, file_extension = os.path.splitext(args.config)

        if file_extension.lower() not in [".yml", ".yaml", ".json"]:
            raise ValueError(
                "Please, specify the --extension parameter with json, yaml, or yml. Alternatively, append the file format of your file for the --config parameter."
            )

    if args.gen == "generate_schema":
        generate_schema(args.config)
    if args.gen == "generate_kg":
        generate_kg(args.config)
    if args.gen == "generate":
        generate(args.config)
