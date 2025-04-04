import re


def parse_user_intent(text):
    # Identify basic service request
    service_type = extract_service_type(text)
    resources = extract_resources(text)
    scaling = extract_scaling_options(text)

    return {
        "service_type": service_type,
        "resources": resources,
        "scaling": scaling if has_scaling(text) else None
    }


def extract_service_type(text):
    # Match common service patterns
    nodejs_patterns = [r'node(?:\.js)?', r'javascript server']
    python_patterns = [r'python', r'flask', r'django']

    # Check for Node.js
    for pattern in nodejs_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            version_match = re.search(
                r'node(?:\.js)?\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            version = version_match.group(1) if version_match else 'latest'
            return f"node:{version}"

    # Check for Python
    for pattern in python_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            version_match = re.search(
                r'python\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            version = version_match.group(1) if version_match else '3.9'
            return f"python:{version}"

    return "alpine:latest"  # Default fallback


def extract_resources(text):
    resources = {}

    # Look for memory specifications
    memory_match = re.search(r'(\d+)\s*(?:GB|MB|gb|mb)', text)
    if memory_match:
        memory_value = memory_match.group(1)
        memory_unit = memory_match.group(2).upper()
        resources["memory"] = f"{memory_value}{memory_unit}"
    else:
        resources["memory"] = "512MB"  # Default value

    # Look for CPU specifications
    cpu_match = re.search(
        r'(\d+(?:\.\d+)?)\s*(?:cpu|cores?)', text, re.IGNORECASE)
    if cpu_match:
        resources["cpu"] = cpu_match.group(1)
    else:
        resources["cpu"] = "1"  # Default value

    return resources


def extract_scaling_options(text):
    scaling = {}

    # Check for min instances
    min_match = re.search(
        r'min(?:imum)?\s*(?:of)?\s*(\d+)\s*instances?', text, re.IGNORECASE)
    if min_match:
        scaling["min"] = int(min_match.group(1))
    else:
        scaling["min"] = 1  # Default

    # Check for max instances
    max_match = re.search(
        r'max(?:imum)?\s*(?:of)?\s*(\d+)\s*instances?', text, re.IGNORECASE)
    if max_match:
        scaling["max"] = int(max_match.group(1))
    else:
        scaling["max"] = 3  # Default

    return scaling


def has_scaling(text):
    return re.search(r'auto[ -]?scal(?:e|ing)', text, re.IGNORECASE) is not None
