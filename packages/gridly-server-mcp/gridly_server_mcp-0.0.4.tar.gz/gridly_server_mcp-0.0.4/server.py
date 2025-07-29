from app.mcpserver import mcp
import app.gridly

def main():
    mcp.run(transport="stdio")

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")