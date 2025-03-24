from enum import Enum
from pathlib import Path

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader


class PDFLoaderType(Enum):
    """Enumeration for different types of PDF loaders."""

    PYPDF = "pypdf"
    UNSTRUCTURED = "unstructured"


class PDFLoader:
    """
    A class to load PDF documents using different loader types.

    Attributes:
        loader_type (PDFLoaderType): The type of loader to use.
        loader_kwargs (dict): Additional keyword arguments for the loader.
    """

    def __init__(self, loader_type: PDFLoaderType, **loader_kwargs):
        """
        Initializes the PDFLoader with the specified loader type and arguments.

        Args:
            loader_type (PDFLoaderType): The type of loader to use.
            **loader_kwargs: Additional keyword arguments for the loader.
        """
        self.loader_type = loader_type
        self.loader_kwargs = loader_kwargs

    def load(self, file_path: Path) -> list[Document]:
        """
        Loads a PDF document from the specified file path.

        Args:
            file_path (Path): The path to the PDF file.

        Returns:
            list[Document]: A list of Document objects loaded from the PDF.

        Raises:
            ValueError: If an unsupported loader type is specified.
        """
        if self.loader_type == PDFLoaderType.PYPDF:
            loader = PyPDFLoader(str(file_path), **self.loader_kwargs)
        elif self.loader_type == PDFLoaderType.UNSTRUCTURED:
            loader = UnstructuredPDFLoader(str(file_path), **self.loader_kwargs)
        else:
            raise ValueError(f"Unsupported loader type: {self.loader_type}")
        return loader.load()
