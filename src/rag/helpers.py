from typing import TYPE_CHECKING, List
import base64

if TYPE_CHECKING:
    from langchain_core.documents import Document
    
    
def parse_documents_content(
    documents: List["Document"],
    k: int = 5
) -> str:
    if len(documents) > k:
        documents = documents[:k]
    return "\n\n".join([document.page_content for document in documents])


def get_gigachat_auth_key(
    client_id: str,
    client_secret: str
) -> str:
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return encoded_credentials
