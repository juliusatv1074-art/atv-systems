#!/usr/bin/env python3

authlogs = {}
keys = ["error", "warning", "denied", "failed", "blocked"]

try:
    with open("/var/log/auth.log", "r") as logs:
        for lines in logs:
            for key in keys:
                if key in lines.lower():
                    authlogs[key] = authlogs.get(key, 0) + 1
except FileNotFoundError:
       print("Error: Log file not found")
      

def sum_report():
    print("\n==============================")
    print("Log Analysis Report")
    print("==============================")
    for key in keys:
        count = authlogs.get(key,0)
        print(f"{key}: {count}")

def save_report():
    with open("log_report.txt", "w") as f:
        for key in keys:
            count = authlogs.get(key, 0)
            f.write(f"{key}: {count}\n")

        total = sum(authlogs.values())
        print(f"\nTotal issues found: {total}")

sum_report()
save_report()
   

