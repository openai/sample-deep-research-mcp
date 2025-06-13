import json
from pathlib import Path
from fastmcp.server import FastMCP

RECORDS = json.loads(Path(__file__).with_name("records.json").read_text())
LOOKUP = {r["id"]: r for r in RECORDS}


def create_server():
    mcp = FastMCP(name="Cupcake MCP", instructions="Search cupcake orders")

    @mcp.tool()
    async def search(query: str):
        """
        Search for cupcake orders – keyword match.
        """
        toks = query.lower().split()
        results = []
        for r in RECORDS:
            hay = " ".join(
                [
                    r.get("title", ""),
                    r.get("text", ""),
                    " ".join(r.get("metadata", {}).values()),
                ]
            ).lower()
            if any(t in hay for t in toks):
                results.append({
                    "id": r["id"],
                    "title": r["title"],
                    "text": r["text"],
                })
        return {"results": results}

    @mcp.tool()
    async def fetch(id: str):
        """
        Fetch a cupcake order by ID.
        """
        if id not in LOOKUP:
            raise ValueError("unknown id")
        return LOOKUP[id]

    return mcp


if __name__ == "__main__":
    create_server().run(transport="sse", host="127.0.0.1", port=8000)
