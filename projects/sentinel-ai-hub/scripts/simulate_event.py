import os
import json
import asyncio
import sys
from dotenv import load_dotenv
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

async def send_event(event_type, city, severity, details):
    load_dotenv()
    
    connection_str = os.getenv("EVENTHUB_CONNECTION_STR")
    eventhub_name = os.getenv("EVENTHUB_NAME")

    if not connection_str:
        print("Error: EVENTHUB_CONNECTION_STR not found.")
        return

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, 
        eventhub_name=eventhub_name
    )
    
    async with producer:
        event_batch = await producer.create_batch()
        
        event_data = {
            "event_type": event_type,
            "city": city,
            "severity": int(severity),
            "details": details
        }

        event_batch.add(EventData(json.dumps(event_data)))
        await producer.send_batch(event_batch)
        print(f"\n🚀 SENTINEL ALERT TRIGGERED")
        print(f"Type: {event_type} | City: {city} | Severity: {severity}\n")

if __name__ == "__main__":
    # Example: python3 scripts/simulate_event.py "Strike" "Miami" 8 "Dock workers strike starting at midnight"
    if len(sys.argv) < 5:
        print("\n[!] Error: Missing event arguments.")
        print("Usage: python3 scripts/simulate_event.py <Type> <City> <Severity> <Details>")
    else:
        asyncio.run(send_event(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
