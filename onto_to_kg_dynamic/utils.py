from typing import Any

from base_ontology.node import BaseNode
from pydantic import BaseModel, Field, create_model


def node_dict_to_ontology(node_dict: dict[str, tuple[type[BaseNode], bool, str]]) -> type[BaseModel]:
    fields: dict[str, Any] = {}

    for key, (node_class, multiplicity, description) in node_dict.items():
        field_name = key.lower().replace("node", "") + ("_nodes" if multiplicity else "_node")
        if multiplicity:
            #! This is a hack to make the list type work with mypy
            fields[field_name] = (list[node_class], Field(default=None, description=description))  # type: ignore
        else:
            fields[field_name] = (node_class, Field(default=None, description=description))

    model = create_model("EntityOntology", **fields)
    return model
