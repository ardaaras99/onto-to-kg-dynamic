from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from base_ontology.node import BaseNode
from pydantic import BaseModel


class LLMOptions(str, Enum):
    OPENAI_O3_MINI = "o3-mini-2025-01-31"
    OPENAI_GPT4_O1 = "gpt-4o-2024-08-06"


@dataclass
class EntityExtractorConfig:
    file_path: Path
    ontology: type[BaseModel]
    llm_model_name: LLMOptions


@dataclass
class KGExtractorConfig:
    use_found_nodes: bool  #! This will be replaced in production
    node_dict: dict[str, tuple[type[BaseNode], bool, str]]
    relation_dict: dict[str, type[BaseNode]]
    entity_extractor_config: EntityExtractorConfig
