import asyncio
import httpx
import json
import subprocess
import time
import os

async def test_resiliency():
    print("🚀 Starting Resiliency Verification...")
    
    # Start the gateway in the background
    # Ensure PYTHONPATH includes the subproject as 'app'
    subproject_path = os.path.join(os.getcwd(), "projects", "resilient_gateway")
    env = {
        **os.environ, 
        "PYTHONPATH": f"{os.getcwd()}:{subproject_path}"
    }
    process = subprocess.Popen(
        ["python3", "projects/resilient_gateway/app/main.py"],
        env=env
    )
    
    # Wait for gateway to start
    time.sleep(3)
    
    url = "http://localhost:8006/v1/complete"
    payload = {
        "prompt": "Test resiliency",
        "model": "gpt-4o"
    }
    
    async with httpx.AsyncClient() as client:
        print("📝 Sending 5 requests to observe failover...")
        for i in range(5):
            resp = await client.post(url, json=payload, timeout=10)
            data = resp.json()
            print(f"✅ Req {i+1}: Region={data.get('region')} | Status={resp.status_code}")
            
    print("🛑 Shutting down gateway...")
    process.terminate()

if __name__ == "__main__":
    asyncio.run(test_resiliency())
