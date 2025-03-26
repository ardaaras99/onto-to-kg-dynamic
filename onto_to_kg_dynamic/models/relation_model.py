from dataclasses import dataclass
from typing import Any

from base_ontology.node import BaseNode
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class HasRelation(BaseModel):
    value: bool = Field(default=False, description="Bu iki node arasında bir ilişki var mı?")
    reason: str | None = Field(default=None, description="Bu kararı vermenizin sebebi nedir?")
    attributes: dict[str, Any] = Field(default_factory=lambda: {}, description="Bu ilişkinin özellikleri")


@dataclass
class ChainInputforRelation:
    input_text: str
    source_node: BaseNode
    target_node: BaseNode
    candidate_relation: str | None = Field(default=None, description="İlişki adayı")


class RelationExtractor:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=HasRelation)
        self.llm = ChatOpenAI(model="o3-mini-2025-01-31")
        template = """
            Aşağıda yer alan iki node arasında candidate olarak verilen ilişki var mıdır? Texte bakarak karar veriniz:
            Text: {input_text}
            target_node: {target_node}
            source_node: {source_node}
            candidate relation: {candidate_relation}
            {format_instructions}
        """
        self.prompt_template = PromptTemplate(
            template=template,
            input_variables=["input_text", "target_node", "source_node", "candidate_relation"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

    def pipeline(self, chain_input_dict: ChainInputforRelation) -> HasRelation:
        self.chain = self.prompt_template | self.llm
        content = str(self.chain.invoke(input=chain_input_dict.__dict__).content)
        has_relation_pydantic_instance = self.parser.parse(content)
        return has_relation_pydantic_instance
