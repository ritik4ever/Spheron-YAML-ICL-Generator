import yaml
import re


def validate_yaml(yaml_string):
    try:
        # Parse the YAML to ensure it's valid YAML syntax
        yaml_dict = yaml.safe_load(yaml_string)

        # Basic ICL validation
        errors = []

        # Check for required top-level keys
        if not yaml_dict.get("version"):
            errors.append("Missing required 'version' field")

        if not yaml_dict.get("services"):
            errors.append("Missing required 'services' field")
        elif not isinstance(yaml_dict["services"], dict):
            errors.append("'services' must be a mapping")
        elif not yaml_dict["services"]:
            errors.append("At least one service must be defined")

        # Validate services
        for service_name, service_config in yaml_dict.get("services", {}).items():
            service_errors = validate_service(service_name, service_config)
            errors.extend(service_errors)

        if errors:
            return {
                "valid": False,
                "errors": errors
            }
        else:
            return {
                "valid": True
            }
    except yaml.YAMLError as e:
        return {
            "valid": False,
            "errors": [f"Invalid YAML syntax: {str(e)}"]
        }
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"]
        }


def validate_service(service_name, service_config):
    errors = []

    # Check for required service properties
    if not service_config.get("image"):
        errors.append(
            f"Service '{service_name}' is missing required 'image' field")

    # Validate resources
    if "resources" in service_config:
        resources = service_config["resources"]

        # Validate memory
        if "memory" in resources:
            memory = resources["memory"]
            if not re.match(r'^\d+[MG]B$', memory):
                errors.append(
                    f"Invalid memory format '{memory}'. Must be in format '1GB' or '512MB'")

        # Validate CPU
        if "cpu" in resources:
            cpu = resources["cpu"]
            try:
                cpu_value = float(cpu)
                if cpu_value <= 0:
                    errors.append(f"CPU value must be positive, got '{cpu}'")
            except ValueError:
                errors.append(f"Invalid CPU value '{cpu}'. Must be a number")

    # Validate autoscaling if present
    if "autoscaling" in service_config:
        autoscaling = service_config["autoscaling"]

        if "min_instances" in autoscaling:
            try:
                min_instances = int(autoscaling["min_instances"])
                if min_instances < 1:
                    errors.append(
                        f"min_instances must be at least 1, got {min_instances}")
            except ValueError:
                errors.append(
                    f"Invalid min_instances value '{autoscaling['min_instances']}'. Must be an integer")

        if "max_instances" in autoscaling:
            try:
                max_instances = int(autoscaling["max_instances"])
                min_instances = int(autoscaling.get("min_instances", 1))
                if max_instances < min_instances:
                    errors.append(
                        f"max_instances ({max_instances}) must be >= min_instances ({min_instances})")
            except ValueError:
                errors.append(
                    f"Invalid max_instances value '{autoscaling['max_instances']}'. Must be an integer")

    return errors
