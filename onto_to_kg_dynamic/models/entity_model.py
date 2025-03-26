from base_ontology.node import BaseNode
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from onto_to_kg_dynamic.models.configurations import EntityExtractorConfig


class EntityExtractor:
    def __init__(self, config: EntityExtractorConfig):
        self.config = config
        self.llm = ChatOpenAI(model=config.llm_model_name.value)
        self.parser = PydanticOutputParser(pydantic_object=self.config.ontology)
        self.prompt_template = self._create_prompt()
        self.chain = self.prompt_template | self.llm

    def pipeline(self) -> list[BaseNode]:
        document = self._load_pdf()
        content = str(self.chain.invoke({"input_text": document.page_content}).content)
        entity_ontology_instance = self.parser.parse(content)
        # define the type of the instance
        return self._extract_nodes_from_instance(entity_ontology_instance)

    @staticmethod
    def _extract_nodes_from_instance(instance: BaseModel) -> list[BaseNode]:
        found_nodes_list: list[BaseNode] = []
        for key in instance.__dict__.keys():
            if key.endswith("_node"):
                found_nodes_list.append(getattr(instance, key))
            elif key.endswith("_nodes"):
                found_nodes_list.extend(getattr(instance, key))
        return found_nodes_list

    def _load_pdf(self) -> Document:
        ##! Currently list[Document] is not supported
        """Load the PDF file specified in the config."""
        pdf_loader = UnstructuredPDFLoader(self.config.file_path, mode="single")
        document = pdf_loader.load()[0]
        return document

    def _create_prompt(self) -> PromptTemplate:
        """Create the prompt template based on configuration."""
        return PromptTemplate(
            template="""
                Sana format instructions ve input olarak bir metin vereceğim, metinden bu formatta bir bilgi grafiği üretmeni istiyorum. Bilgi grafiğinde metinde geçen tüm ilgili detayları yüksek doğrulukla yakalamalısın, metinde açıkça belirtilmeyen herhangi bir bilgi eklememelisin.
                İlk olarak düğümleri (nodes) çıkaracaksın daha sonra bu düğümler arasındaki relationları çıkırmış olduğun nodelar ile doldurmanı istiyorum. Yeniden yaratmaya çalışmana gerek yok.
                {format_instructions}

                Aşağıdaki hukuki sözleşme metnine dayanarak, ilgili bilgi grafiğini üret:
                Girdi: {input_text}

                """,
            input_variables=["input_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
