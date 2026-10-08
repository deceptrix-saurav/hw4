from pathlib import Path
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
try:
    from .models import ChatReply, ProductCard, StockResult
    from .tools import search_products, lookup_price, lookup_stock
except ImportError:
    from models import ChatReply, ProductCard, StockResult
    from tools import search_products, lookup_price, lookup_stock

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / ".env")
load_dotenv(ROOT / ".env")
PROMPT = (ROOT / "prompts" / "prompt.md").read_text(encoding="utf-8")

class AgentDeps:
    def __init__(self, user: dict | None = None, page_context: str | None = None): self.user, self.page_context = user, page_context

def build_agent() -> Agent:
    client = AsyncOpenAI(api_key=os.environ["PORTKEY_API_KEY"], base_url="https://api.portkey.ai/v1", default_headers={"x-portkey-provider": "openai"})
    model = OpenAIChatModel(os.getenv("CAMPUS_CUSTOMS_MODEL", "gpt-5.6-luna"), provider=OpenAIProvider(openai_client=client))
    agent = Agent(model, output_type=ChatReply, system_prompt=PROMPT)
    @agent.tool
    def find_products(ctx: RunContext[AgentDeps], query: str) -> list[ProductCard]:
        """Find Campus Customs products relevant to the shopper's request."""
        return search_products(query)
    @agent.tool
    def get_price(ctx: RunContext[AgentDeps], product_id: str) -> ProductCard | None:
        """Look up the exact catalogue price; never estimate it."""
        return lookup_price(product_id)
    @agent.tool
    def get_stock(ctx: RunContext[AgentDeps], product_id: str, size: str | None = None) -> StockResult:
        """Look up real inventory quantities, optionally for one requested size."""
        return lookup_stock(product_id, size)
    return agent

agent = build_agent() if os.getenv("PORTKEY_API_KEY") else None

async def chat(message: str, deps: AgentDeps | None = None) -> ChatReply:
    if agent is None:
        return ChatReply(message="I’m ready to help you find Yale gear. The concierge connection is waiting for its API configuration.", products=search_products(message))
    context = f"Customer context: {deps.user if deps else None}; page context: {deps.page_context if deps else None}"
    result = await agent.run(f"{context}\nShopper message: {message}", deps=deps or AgentDeps())
    return result.output

