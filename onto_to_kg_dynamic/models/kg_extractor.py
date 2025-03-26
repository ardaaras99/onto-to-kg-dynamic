from base_ontology.node import BaseNode
from base_ontology.relation import BaseRelation

from onto_to_kg_dynamic.models.configurations import KGExtractorConfig
from onto_to_kg_dynamic.models.entity_model import EntityExtractor
from onto_to_kg_dynamic.models.relation_model import ChainInputforRelation, HasRelation, RelationExtractor


class KGExtractor:
    def __init__(self, config: KGExtractorConfig):
        self.config = config
        self.entity_extractor = EntityExtractor(config=config.entity_extractor_config)
        self.relation_extractor = RelationExtractor()

    def pipeline(self) -> tuple[list[BaseNode], list[BaseRelation]]:
        if self.config.use_found_nodes:
            from example_ontology.found_nodes import found_nodes

            found_nodes = EntityExtractor._extract_nodes_from_instance(found_nodes)
        else:
            found_nodes = self.entity_extractor.pipeline()
        found_relations = self._find_relations_between_nodes(found_nodes)

        return found_nodes, found_relations

    def _find_relations_between_nodes(self, found_nodes: list[BaseNode]) -> list[BaseRelation]:
        found_relations = []
        for _, relation_class in self.config.relation_dict.items():
            source_class = relation_class.model_fields["source_node"].annotation
            target_class = relation_class.model_fields["target_node"].annotation
            source_nodes = [node for node in found_nodes if isinstance(node, source_class)]
            target_nodes = [node for node in found_nodes if isinstance(node, target_class)]

            if not source_nodes or not target_nodes:
                pass
            else:
                print(f"There are total of {len(source_nodes)} {source_class.__name__} and {len(target_nodes)} {target_class.__name__} nodes.")
                print(f"Trying for the relation: {source_class.__name__} -> {relation_class.__name__} -> {target_class.__name__}")
                for source_node in source_nodes:
                    for target_node in target_nodes:
                        has_relation = self._check_relation(source_node, target_node, relation_class.__name__)
                        if has_relation.value:
                            print(f"""Relation found between {source_node.__class__.__name__}
                            and {target_node.__class__.__name__} with the relation {relation_class.__name__}""")
                            found_relations.append(
                                relation_class(
                                    source_node=source_node,
                                    target_node=target_node,
                                    attributes=has_relation.attributes,
                                    reason=has_relation.reason,
                                )
                            )
                print("******************", end="\n\n")
        return found_relations

    def _check_relation(self, source_node: BaseNode, target_node: BaseNode, candidate_relation: str) -> HasRelation:
        chain_input = ChainInputforRelation(
            input_text=" ".join([source_node.reference_text, target_node.reference_text]),
            source_node=source_node,
            target_node=target_node,
            candidate_relation=candidate_relation,
        )
        has_relation = self.relation_extractor.pipeline(chain_input)
        return has_relation
