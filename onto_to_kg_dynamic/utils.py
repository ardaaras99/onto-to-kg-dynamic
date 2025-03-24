from pydantic import BaseModel, Field, create_model

from onto_to_kg_dynamic.base_ontology import BaseNode


def node_list_to_ontology(pydantic_node_list: list[tuple[type[BaseNode], bool, str]]) -> type[BaseModel]:
    node_dict = {}
    for node_class, multiplicty, description in pydantic_node_list:
        node_dict[node_class.__name__] = (node_class, multiplicty, description)
    EntityOntology = node_dict_to_ontology(node_dict)
    return EntityOntology


def node_dict_to_ontology(node_dict: dict[str, tuple[type[BaseNode], bool, str]]) -> type[BaseModel]:
    fields = {}
    for key, (node_class, multiplicity, description) in node_dict.items():
        field_name = key.lower().replace("node", "") + ("_nodes" if multiplicity else "_node")
        if multiplicity:
            fields[field_name] = (list[node_class], Field(default=None, description=description))
        else:
            fields[field_name] = (node_class, Field(default=None, description=description))

    return create_model("EntityOntology", **fields)
