from pydantic import BaseModel, Field

class ProductCard(BaseModel):
    id: int | str
    name: str
    price: float
    description: str
    image: str
    stock: int | None = None

class ChatReply(BaseModel):
    message: str
    products: list[ProductCard] = Field(default_factory=list)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    user: dict | None = None
    page_context: str | None = None
    history: list[dict] = Field(default_factory=list)

