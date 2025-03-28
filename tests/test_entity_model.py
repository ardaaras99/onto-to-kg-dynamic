from datetime import datetime
from pathlib import Path

import pytest
from base_ontology.node import BaseNode
from pydantic import BaseModel, Field, create_model

from onto_to_kg_dynamic.models.configurations import EntityExtractorConfig, LLMOptions
from onto_to_kg_dynamic.models.entity_model import EntityExtractor
from onto_to_kg_dynamic.utils import node_dict_to_ontology


@pytest.fixture
def sample_pdf_path() -> Path:
    return Path("/Users/ardaaras/cybersoft/onto-to-kg-dynamic/data/short.pdf")


@pytest.fixture
def sözleşme_node() -> type[BaseNode]:
    return create_model(
        "SözleşmeNode",
        başlık=(str | None, Field(default=None, description="Sözleşme başlığı, ilk sayfada bulunur")),
        tür=(str | None, Field(default=None, description="Sözleşme türü (örneğin: kira sözleşmesi, satış sözleşmesi)")),
        amaç=(str | None, Field(default=None, description="Sözleşmenin amacı")),
        bağlı_olduğu_kanun=(str | None, Field(default=None, description="Sözleşmenin bağlı olduğu kanun")),
        bağlı_olduğu_yönetmelik=(str | None, Field(default=None, description="Sözleşmenin bağlı olduğu yönetmelik")),
        bağlı_olduğu_yönerge=(str | None, Field(default=None, description="Sözleşmenin bağlı olduğu yönerge")),
        __base__=BaseNode,
    )


@pytest.fixture
def kira_süresi_node() -> type[BaseNode]:
    return create_model(
        "KiraSüresiNode",
        başlangıç_tarihi=(datetime | None, Field(default=None, description="Kira sözleşmesinin başlangıç tarihi (format: YYYY-MM-DD)")),
        kira_süresi=(int | None, Field(default=None, description="Kira süresi (ay cinsinden), x ay şeklinde yaz")),
        bitiş_tarihi=(datetime | None, Field(default=None, description="Kira sözleşmesinin bitiş tarihi (format: YYYY-MM-DD), başlangıç tarihi ve kira süresi verilmişse bu alan otomatik hesaplanır")),
        erken_bitebilir=(bool | None, Field(default=None, description="Kira sözleşmesi normal bitiş tarihinden farklılık gösterebilir mi?")),
        erken_bitebilir_açıklaması=(str | None, Field(default=None, description="Kira sözleşmesinin bitiş tarihi değişiklik gösterebilir ise açıklaması")),
        __base__=BaseNode,
    )


@pytest.fixture
def entity_ontology(sözleşme_node: type[BaseNode], kira_süresi_node: type[BaseNode]) -> type[BaseModel]:
    node_list = [
        (sözleşme_node, False, "Sözleşmenin kendisine ait olan Node"),
        (kira_süresi_node, False, "Kira Süresi ile alakalı her şeyi tutan Node"),
    ]
    node_dict = {node.__name__: (node, is_relation, description) for node, is_relation, description in node_list}

    return node_dict_to_ontology(node_dict)


@pytest.fixture
def entity_extractor_config(sample_pdf_path: Path, entity_ontology: type[BaseModel]) -> EntityExtractorConfig:
    return EntityExtractorConfig(
        file_path=sample_pdf_path,
        ontology=entity_ontology,
        llm_model_name=LLMOptions.OPENAI_O3_MINI,
    )


@pytest.mark.parametrize("llm_model", [LLMOptions.OPENAI_O3_MINI, LLMOptions.OPENAI_GPT4_O1])
def test_entity_extractor_with_different_llms(entity_extractor_config: EntityExtractorConfig, llm_model: LLMOptions) -> None:
    """Test EntityExtractor with different LLM models"""
    entity_extractor_config.llm_model_name = llm_model
    entity_extractor = EntityExtractor(entity_extractor_config)
    result = entity_extractor.pipeline()

    # Verify the result structure
    assert isinstance(result, list)
    assert all(isinstance(node, BaseNode) for node in result)
