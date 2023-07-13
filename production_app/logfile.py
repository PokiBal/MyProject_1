import logging

with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    entry = last_line.strip().split(":")
    timestamp = ":".join(entry[:2])
    message = entry[4].strip().replace('"', '\\"')

print(f"{timestamp}, {message}")
