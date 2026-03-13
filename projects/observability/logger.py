
import time

def log_call(prompt, response):
    print({
        "prompt": prompt,
        "response": response,
        "timestamp": time.time()
    })
