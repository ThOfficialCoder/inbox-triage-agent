import os
from tavily import TavilyClient

client = TavilyClient(os.environ.get("TAVILY_API_KEY"))

response = client.search(
    query="latest AI hackathon news",
    search_depth="basic"
)

print(response)