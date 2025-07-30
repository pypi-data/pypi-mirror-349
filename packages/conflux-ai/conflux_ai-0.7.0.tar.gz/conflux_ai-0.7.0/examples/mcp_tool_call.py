import asyncio

from conflux import HandlerChain, Message, handler
from conflux.handlers import McpToolCall, OpenAiLLM

config = {
    "mcpServers": {
        "explorer": {"url": "http://localhost:9000/mcp/sse", "transportType": "sse"}
    }
}


@handler
async def fetch_tool_list(msg: Message, chain: HandlerChain) -> str:
    chain.variables["query"] = msg.primary
    return f"User query: {msg.primary}?"


@handler
async def answer(msg: Message, chain: HandlerChain) -> str:
    return f"Answer the following query:\n{chain.variables['query']}\n\nHere is a result of appropriate tool for the query:\n{msg}\n\nAnswer the query using the tool result."


def main():
    chain = (
        fetch_tool_list
        >> McpToolCall(config=config, llm=OpenAiLLM)
        >> answer
        >> OpenAiLLM()
    )
    return asyncio.run(
        chain.run(
            "Get all the columns of /workspace/input/sdtm/ae.csv",
        )
    )


if __name__ == "__main__":
    result = main()
    print(result)
