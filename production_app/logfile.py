with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    entry = last_line.strip().split(":")
    if len(entry) < 5:
        print("Unexpected log format.")
        timestamp = "Unknown"
        message = "Unknown"
    else:
        timestamp = ":".join(entry[:2])
        message = entry[4].strip().replace('"', '\\"')

print(f"{timestamp}, {message}")
