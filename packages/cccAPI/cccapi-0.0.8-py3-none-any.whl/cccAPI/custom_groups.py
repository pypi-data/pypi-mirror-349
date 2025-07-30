# Configure logging
import logging
logger = logging.getLogger("cccAPI")
import os
import json

class cccAPICustomGroups:
    def __init__(self, connection):
        """Handles CCC Custom Groups API endpoints."""
        self.connection = connection
        # Load allowed fields from customgroup.json
        schema_path = os.path.join(os.path.dirname(__file__), "schemas", "CustomGroup.json")
        try:
            with open(schema_path, "r") as f:
                schema = json.load(f)
                # Assume properties at the root level
                self.allowed_fields = set(schema.get("properties", {}).keys())
        except Exception as e:
            logger.warning(f"Could not load customgroup.json schema: {e}")
            self.allowed_fields = set()
    
    # 4.2.9. Lists all groups
    def show_customgroups(self, params=None):
        """
        Retrieve current custom groups with optional query parameters.

        :param params: Dictionary of query parameters to include in the request.
                       Example: {"fields": "name,id,uuid,etag"}
        :return: API response containing current custom groups.
        """
        if params is None:
            params = {}

        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            invalid_fields = requested_fields - self.allowed_fields
            if invalid_fields:
                raise ValueError(
                    f"Invalid fields requested: {', '.join(invalid_fields)}. "
                    f"Allowed fields are: {', '.join(self.allowed_fields)}"
                )
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = None

        return self.connection.get("customgroups", params=params)
    
    # 4.2.1. Gets all nodes of an existing group
    def show_nodes_in_customgroup(self, identifier, params=None):
        """
        Retrieve current set of nodes in {identifier} custom group with optional query parameters.

        :param identifier: The identifier of the custom group (UUID or name).
        :param params: Dictionary of query parameters to include in the request.
                       Example: {"fields": "name,id,uuid,etag"}
        :return: API response containing current custom groups.
        """
        if params is None:
            params = {}

        if not isinstance(identifier, str):
            raise ValueError("The 'identifier' parameter must be a string.")

        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            #invalid_fields = requested_fields - self.allowed_fields
            #if invalid_fields:
            #    raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}. Allowed fields are: {', '.join(self.allowed_fields)}")
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = None

        return self.connection.get(f"customgroups/{identifier}/nodes", params=params)