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