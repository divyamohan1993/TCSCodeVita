import pandas as pd
import re

file_path = input()
data = pd.read_csv(file_path)

def is_sql_injection(payload):
    patterns = [
        "UNION SELECT",
        "or 1=1",
        "SELECT",
        "UPDATE",
        "DELETE",
        "INSERT",
        "DROP",
        "%27", "'", "--", "%23", "#",
        "exec xp_"
    ]
    for pat in patterns:
        if pat.lower() in payload.lower():
            return True
    return False

sql_injection_attempts = []

for idx, row in data.iterrows():
    info = str(row["Info"])
    source_ip = str(row["Source"])
    parts = info.split()
    if len(parts) >= 3:
        method = parts[0]
        uri = parts[1]
        http_ver = parts[2]
        if method in ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS"] and http_ver.startswith("HTTP"):
            if is_sql_injection(uri):
                sql_injection_attempts.append((row["No."], row["Time"], source_ip, uri))

if len(sql_injection_attempts) == 0:
    print("1A: NULL")
    print("2A: 0")
    print("3A: NULL")
    print("4A: NULL")
    print("5A: 0")
else:
    sql_injection_attempts.sort(key=lambda x: x[0])
    attacker_ip = sql_injection_attempts[0][2]
    total_attempts = len(sql_injection_attempts)
    first_payload = sql_injection_attempts[0][3]
    last_payload = sql_injection_attempts[-1][3]
    count_colon = 0
    for attempt in sql_injection_attempts:
        if ":" in attempt[3] or "0x3a" in attempt[3]:
            count_colon += 1

    print("1A:", attacker_ip)
    print("2A:", total_attempts)
    print("3A:", first_payload)
    print("4A:", last_payload)
    print("5A:", count_colon)
