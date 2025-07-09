from mcp.server.fastmcp import FastMCP
from agent import data_visualization_agent, save_image_data

mcp = FastMCP("AI_Agent", host="127.0.0.1", port=5000, debug=True, verbose=True)


@mcp.tool()
async def visualize_data(csv_file_path: str, user_query: str):
    """Function to visualize data based on a CSV file and user query."""
    return data_visualization_agent(csv_file_path, user_query)


if __name__ == "__main__":
    mcp.run(transport="sse")
