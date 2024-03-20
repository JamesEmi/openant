import datetime

# Replace the timestamp with the one you have

timestamp = 1709763391668385024

# Convert timestamp to datetime object
timestamp_in_seconds = timestamp / 10**9  # Convert nanoseconds to seconds
date_time = datetime.datetime.fromtimestamp(timestamp_in_seconds)

# Format datetime object into a readable string
formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

print("Timestamp in human-readable format:", formatted_date_time)
