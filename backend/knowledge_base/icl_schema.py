# backend/knowledge_base/icl_schema.py
ICL_SCHEMA = {
    "version": {
        "type": "string",
        "required": True,
        "description": "ICL schema version"
    },
    "services": {
        "type": "object",
        "required": True,
        "description": "Definition of services to deploy",
        "properties": {
            "*": {  # Any service name
                "type": "object",
                "properties": {
                    "image": {
                        "type": "string",
                        "required": True,
                        "description": "Docker image"
                    },
                    "resources": {
                        "type": "object",
                        "properties": {
                            "memory": {
                                "type": "string",
                                "pattern": r"^\d+[MG]B$",
                                "description": "Memory allocation (e.g., '512MB', '1GB')"
                            },
                            "cpu": {
                                "type": "string",
                                "description": "CPU allocation (e.g., '0.5', '1', '2')"
                            }
                        }
                    },
                    "autoscaling": {
                        "type": "object",
                        "properties": {
                            "min_instances": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Minimum number of instances"
                            },
                            "max_instances": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Maximum number of instances"
                            }
                        }
                    }
                }
            }
        }
    }
}
