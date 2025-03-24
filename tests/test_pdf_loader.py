from pathlib import Path

import pytest
from langchain.schema import Document

from onto_to_kg_dynamic.pdf_loader import PDFLoader, PDFLoaderType


@pytest.fixture
def sample_pdf_path():
    return Path("/Users/ardaaras/cybersoft/onto-to-kg-dynamic/data/long.pdf")


@pytest.fixture
def sample_unstructured_pdf_path():
    return Path("/Users/ardaaras/cybersoft/onto-to-kg-dynamic/data/long.pdf")


def test_pypdf_loader(sample_pdf_path):
    # Test the PyPDFLoader
    loader = PDFLoader(loader_type=PDFLoaderType.PYPDF)
    documents = loader.load(sample_pdf_path)
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)


def test_unstructured_pdf_loader(sample_unstructured_pdf_path):
    # Test the UnstructuredPDFLoader
    loader = PDFLoader(loader_type=PDFLoaderType.UNSTRUCTURED)
    documents = loader.load(sample_unstructured_pdf_path)
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)
