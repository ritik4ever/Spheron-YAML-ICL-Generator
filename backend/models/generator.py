import yaml


def generate_yaml(parsed_requirements):
    # Start with basic structure
    yaml_dict = {
        "version": "1.0",
        "services": {}
    }

    # Add service based on requirements
    service_name = "app"
    service_config = {
        "image": parsed_requirements["service_type"],
        "resources": {
            "memory": parsed_requirements["resources"]["memory"],
            "cpu": parsed_requirements["resources"].get("cpu", "1")
        }
    }

    # Add scaling if specified
    if parsed_requirements["scaling"]:
        service_config["autoscaling"] = {
            "min_instances": parsed_requirements["scaling"].get("min", 1),
            "max_instances": parsed_requirements["scaling"].get("max", 3)
        }

    # Add the service to the services dictionary
    yaml_dict["services"][service_name] = service_config

    # Convert to YAML string
    return yaml.dump(yaml_dict, default_flow_style=False)
