from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from onto_to_kg_dynamic.pdf_loader import PDFLoaderType


class LLMOptions(str, Enum):
    OPENAI_O3_MINI = "o3-mini-2025-01-31"
    OPENAI_GPT4_O1 = "gpt-4o-2024-08-06"


@dataclass
class EntityExtractorConfig:
    file_path: Path
    ontology: type[BaseModel]
    llm_model_name: LLMOptions
    pdf_loader_type: PDFLoaderType
    pdf_loader_kwargs: dict[str, Any]
