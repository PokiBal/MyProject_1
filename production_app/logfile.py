with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    last_line = last_line.rstrip('\n')  # remove new line characters
    entry = last_line.strip().split(" - ")
    if len(entry) < 4:
        print("Unexpected log format.")
        timestamp = "Unknown"
        message = "Unknown"
    else:
        timestamp = entry[0]
        message = entry[4].strip().replace('"', '\\"')

print(f"{timestamp}, {message}")

