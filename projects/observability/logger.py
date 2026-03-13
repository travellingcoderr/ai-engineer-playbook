
import time

def log(prompt, response):
    return {
        "prompt": prompt,
        "response": response,
        "timestamp": time.time()
    }
