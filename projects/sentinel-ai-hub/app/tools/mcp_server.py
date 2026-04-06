from mcp.server.fastmcp import FastMCP
import random

# Create an MCP server for Supply Chain operations
mcp = FastMCP("Sentinel Supply Chain Server")

@mcp.tool()
def get_shipment_status(shipment_id: str) -> str:
    """
    Get the real-time status of a shipment by its ID.
    """
    statuses = ["In Transit", "Delayed due to weather", "Shipped", "Processing", "Delivered"]
    # For demo purposes, we return a deterministic-looking but random status
    status = random.choice(statuses)
    return f"Shipment {shipment_id} status: {status}"

@mcp.tool()
def check_inventory(item_name: str, warehouse_location: str = "Central") -> str:
    """
    Check stock levels for a specific item in a given warehouse.
    """
    levels = ["In Stock (500 units)", "Low Stock (12 units)", "Out of Stock", "In Stock (1200 units)"]
    level = random.choice(levels)
    return f"Item '{item_name}' at {warehouse_location} warehouse: {level}"

@mcp.tool()
def calculate_risk_index(event_type: str, city: str, severity: int) -> float:
    """
    Calculate a disruption risk index (0.0 to 1.0) based on event details.
    Severity should be 1-10.
    """
    # Logic: higher severity = higher risk. 
    # Certain cities might have higher baseline risk for certain events.
    base_risk = 0.1
    if city.lower() in ["miami", "new orleans"] and "hurricane" in event_type.lower():
        base_risk = 0.4
    
    risk = base_risk + (severity / 20.0)
    return min(1.0, risk)

if __name__ == "__main__":
    # In a real scenario, this would run over stdio or SSE.
    # For the multi-agent hub, we might run this in a background process.
    mcp.run()
