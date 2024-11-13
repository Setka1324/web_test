import json

def parse_json_attributes(json_filepath):
    """
    Parses a JSON file and returns a set of all unique attributes found across all entries.
    
    Args:
    json_filepath (str): Path to the JSON file containing the entries.
    
    Returns:
    set: A set containing all unique attributes across entries.
    """
    unique_attributes = set()
    
    # Load JSON data from the file
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    
    # Iterate over each entry in the JSON data
    for entry in data:
        # Update the set of unique attributes with the keys from the current entry
        unique_attributes.update(entry.keys())
    
    return unique_attributes

attributes = parse_json_attributes("companies.json")
print(attributes)
