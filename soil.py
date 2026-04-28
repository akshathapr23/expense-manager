import random
import time
import requests

API_KEY = "A95X3XNQ938OWZNL"

while True:
    # 1. Simulate LDR value (0–1023)
    raw = random.randint(0, 1023)

    # 2. Convert to percentage
    percent = (raw / 1023) * 100

    # 3. Assign light condition
    if percent < 30:
        status = 1   # Dark
    elif percent < 70:
        status = 2   # Dim
    else:
        status = 3   # Bright

    # 4. Send data to ThingSpeak
    url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={raw}&field2={percent}&field3={status}"

    requests.get(url)

    # 5. Print output
    print(f"Raw: {raw} | Light: {round(percent,2)}% | Status: {status}")

    # 6. Wait 15 seconds
    time.sleep(15)