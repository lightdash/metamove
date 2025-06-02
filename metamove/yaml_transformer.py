from ruamel.yaml import YAML

def transform_yaml(input_file: str, output_file: str) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(input_file, 'r') as f:
        data = yaml.load(f)

    def process_node(node):
        if isinstance(node, dict):
            keys = list(node.keys())
            for prop in ['meta', 'tags']:
                if prop in keys:
                    value = node.pop(prop)
                    if 'config' not in node:
                        node['config'] = {}
                        new_keys = []
                        inserted_config = False
                        
                        insertion_point = None
                        if 'config' in keys:
                            insertion_point = keys.index('config')
                        elif 'meta' in keys:
                            insertion_point = keys.index('meta')
                        elif 'tags' in keys:
                            insertion_point = keys.index('tags')
                        
                        for i, key in enumerate(keys):
                            if key not in ['config']:
                                new_keys.append(key)
                            if i == insertion_point and not inserted_config:
                                new_keys.append('config')
                                inserted_config = True
                        
                        if not inserted_config:
                            new_keys.append('config')
                            
                        new_node = {}
                        for k in new_keys:
                            if k in node:
                                new_node[k] = node[k]
                        node.clear()
                        node.update(new_node)
                    if prop in node['config']:
                        if isinstance(node['config'][prop], (dict, list)) and isinstance(value, (dict, list)):
                            if isinstance(value, dict):
                                node['config'][prop] = {**node['config'][prop], **value}
                            else:
                                node['config'][prop] = list(set(node['config'][prop] + value))
                        else:
                            node['config'][prop] = value
                    else:
                        node['config'][prop] = value
                    keys.remove(prop)
                if 'config' not in keys and 'config' in node:
                    keys.append('config')
            for key in keys:
                if key == 'config' and any(p in node['config'] for p in ['meta', 'tags']):
                    config_keys = list(node['config'].keys())
                    for ckey in config_keys:
                        if ckey not in ['meta', 'tags']:
                            process_node(node['config'][ckey])
                else:
                    process_node(node[key])
        elif isinstance(node, list):
            for item in node:
                process_node(item)

    process_node(data)

    with open(output_file, 'w') as f:
        yaml.dump(data, f, transform=lambda node: node) 