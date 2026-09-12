def get_nested(data, key):
    for part in key.split("."):
        data = data[part]
    return data


def set_nested(data, key, value):
    parts = key.split(".")
    
    for part in parts[:-1]:
        data = data[part]
    
    data[parts[-1]] = value


def get_parent(data, key):
    parts = key.split(".")

    for part in parts[:-1]:
        data = data[part]

    return data, parts[-1]


def find_item(data, attribute, value):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if item.get(attribute) == value:
                    return item

    elif isinstance(data, dict):
        for key, item in data.items():
            result = find_item(item, attribute, value)
            if result is not None:
                return result

    return None


