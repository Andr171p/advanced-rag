from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from langchain_core.documents import Document
    
    
def parse_documents_content(
    documents: List["Document"],
    k: int = 5
) -> str:
    if len(documents) > k:
        documents = documents[:k]
    return "\n\n".join([document.page_content for document in documents])
