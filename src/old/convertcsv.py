import json
import csv

# Load the JSON file
with open('obj_props (1).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare result list
rows = []

# Traverse top-level keys
for top_key, properties in data.items():
    # Skip non-dict values or unwanted keys
    if not isinstance(properties, dict):
        continue

    for prop_key, value in properties.items():
        if prop_key in ("$INCLUDE", "UNKNOWN"):
            continue
        # Skip if value is not a list (we only expect list-based entries)
        if not isinstance(value, list):
            continue
        # First column: top-level key, second: property name, then value contents
        rows.append([top_key, prop_key] + value)

# Write to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Category', 'Property', 'Type', 'ID', 'Description'])  # header
    writer.writerows(rows)

print("CSV written to output.csv")