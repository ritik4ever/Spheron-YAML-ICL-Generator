import re
import copy


def parse_refinement_intent(text, current_config):
    refinement = {}

    # Check for memory adjustments
    if re.search(r'(increase|more|higher|larger)\s+memory', text, re.IGNORECASE):
        current_memory = extract_current_memory(current_config)
        refinement["memory"] = increase_memory(current_memory)
    elif re.search(r'(decrease|less|lower|smaller)\s+memory', text, re.IGNORECASE):
        current_memory = extract_current_memory(current_config)
        refinement["memory"] = decrease_memory(current_memory)
    elif memory_match := re.search(r'(\d+)\s*(?:GB|MB|gb|mb)', text):
        memory_value = memory_match.group(1)
        memory_unit = memory_match.group(2).upper()
        refinement["memory"] = f"{memory_value}{memory_unit}"

    # Check for scaling adjustments
    if re.search(r'add\s+(?:auto[ -]?scal(?:e|ing))', text, re.IGNORECASE):
        refinement["add_scaling"] = True

    return refinement


def apply_refinement(current_config, refinement):
    config_copy = copy.deepcopy(current_config)

    if not config_copy.get("services"):
        config_copy["services"] = {"app": {}}

    service_name = next(iter(config_copy["services"]))

    # Apply memory refinement if specified
    if "memory" in refinement:
        if "resources" not in config_copy["services"][service_name]:
            config_copy["services"][service_name]["resources"] = {}
        config_copy["services"][service_name]["resources"]["memory"] = refinement["memory"]

    # Apply scaling refinement if specified
    if refinement.get("add_scaling"):
        config_copy["services"][service_name]["autoscaling"] = {
            "min_instances": 1,
            "max_instances": 3
        }

    return config_copy


def extract_current_memory(config):
    try:
        service_name = next(iter(config.get("services", {})))
        return config["services"][service_name]["resources"]["memory"]
    except (KeyError, StopIteration):
        return "512MB"  # Default


def increase_memory(current_memory):
    # Simple implementation - double memory with cap at 4GB
    match = re.match(r'(\d+)(MB|GB)', current_memory)
    if match:
        value = int(match.group(1))
        unit = match.group(2)

        if unit == "MB":
            if value < 1024:
                return f"{value * 2}MB"
            else:
                return "2GB"
        else:  # GB
            if value < 4:
                return f"{value * 2}GB"
            else:
                return "4GB"

    return "1GB"  # Default if parsing fails


def decrease_memory(current_memory):
    # Simple implementation - halve memory with floor at 256MB
    match = re.match(r'(\d+)(MB|GB)', current_memory)
    if match:
        value = int(match.group(1))
        unit = match.group(2)

        if unit == "MB":
            if value > 256:
                return f"{max(value // 2, 256)}MB"
            else:
                return "256MB"
        else:  # GB
            if value > 1:
                return f"{value // 2}GB"
            else:
                return "512MB"

    return "512MB"  # Default if parsing fails
