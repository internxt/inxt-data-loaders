import collections
import json
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_extract(schema, obj):
    flattened_obj = flatten(obj)
    return {key: flattened_obj[key] for key in schema if key in flattened_obj}


def extract_schema_data(schema, data_list):
    return [flatten_extract(schema, item) for item in data_list]


def flatten_items_list(element_list):
    return [flatten(item) for item in element_list]


def remove_lists(d, key='data'):
    if not isinstance(d, dict):
        return d
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_lists(v, key)
        elif isinstance(v, list) and v:
            v = remove_lists(v[0], key)
        new[k] = v
    return new


def bulk_remove_lists(data_list):
    return [remove_lists(json.loads(str(item))) for item in data_list]
