from typing import Optional, List

from duowen_agent.llm import tokenizer
from pydantic import BaseModel, computed_field


class ToolSearchResultDetails(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    content: str
    site_name: Optional[str] = None
    site_icon: Optional[str] = None
    date_published: Optional[str] = None
    content_split: Optional[str] = None
    content_vector: Optional[list[float]] = None

    @computed_field
    @property
    def content_with_weight(self) -> str:
        return f"URL:{self.url}\nTITLE: {self.title}\nDATE PUBLISHED: {self.date_published}\nCONTENT: {self.content}"

    @computed_field
    @property
    def chat_token(self) -> int:
        return tokenizer.chat_len(self.content_with_weight)

    @computed_field
    @property
    def emb_token(self) -> int:
        return tokenizer.emb_len(self.content_with_weight)


class ToolSearchResult(BaseModel):
    result: Optional[List[ToolSearchResultDetails]] = []

    @computed_field
    @property
    def content_with_weight(self) -> str:
        return "\n\n".join([i.content_with_weight for i in self.result])
