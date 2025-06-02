import pytest
from ruamel.yaml import YAML
from metamove.yaml_transformer import transform_yaml
import os
import tempfile
import re

@pytest.fixture
def yaml():
    y = YAML()
    y.preserve_quotes = True
    y.indent(mapping=2, sequence=4, offset=2)
    return y

def test_basic_meta_tags_transformation(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'meta': {'owner': 'Team'},
            'tags': ['tag1', 'tag2']
        }]
    }
    
    expected_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'meta': {'owner': 'Team'},
                'tags': ['tag1', 'tag2']
            }
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        assert result == expected_data

def test_merge_existing_config(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'config': {'existing': 'value'},
            'meta': {'owner': 'Team'},
            'tags': ['tag1']
        }]
    }
    
    expected_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'existing': 'value',
                'meta': {'owner': 'Team'},
                'tags': ['tag1']
            }
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        assert result == expected_data

def test_nested_meta_tags(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'columns': [{
                'name': 'test_column',
                'meta': {'type': 'string'},
                'tags': ['column']
            }]
        }]
    }
    
    expected_data = {
        'models': [{
            'name': 'test_model',
            'columns': [{
                'name': 'test_column',
                'config': {
                    'meta': {'type': 'string'},
                    'tags': ['column']
                }
            }]
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        assert result == expected_data

def test_config_precedence(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'config': {'existing': 'value'},
            'meta': {'owner': 'Team'},
            'tags': ['tag1'],
            'other': 'field'
        }]
    }
    
    expected_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'existing': 'value',
                'meta': {'owner': 'Team'},
                'tags': ['tag1']
            },
            'other': 'field'
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        assert result == expected_data

def test_merge_meta_tags_values(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'meta': {'existing': 'value'},
                'tags': ['existing']
            },
            'meta': {'new': 'value'},
            'tags': ['new']
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
        model = result['models'][0]
        config = model['config']
        assert set(config['tags']) == {'existing', 'new'}
        assert config['meta']['existing'] == 'value'
        assert config['meta']['new'] == 'value'
        assert model['name'] == 'test_model'

def test_non_dict_meta_values(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'meta': 42,
            'tags': ['tag1']
        }]
    }
    
    expected_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'meta': 42,
                'tags': ['tag1']
            }
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        assert result == expected_data

def test_whitespace_preservation(yaml):
    input_yaml = """
    models:
      - name: test_model
        meta:
          owner: "Team"
          # Preserve this comment
          description: >
            This is a multi-line
            description with
            preserved whitespace
        tags:
          - tag1
          - tag2
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        input_file.write(input_yaml)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = f.read()
        # Check that all lines are present, regardless of indentation
        assert re.search(r'This is a multi-line', result)
        assert re.search(r'description with', result)
        assert re.search(r'preserved whitespace', result)
        # Verify indentation for config and meta
        assert "config:" in result
        assert "meta:" in result

def test_comment_preservation(yaml):
    input_yaml = """
    models:
      - name: test_model
        # This is a top-level comment
        meta:
          # This is a meta comment
          owner: "Team"
        tags:
          # This is a tags comment
          - tag1
          - tag2
        # This is a trailing comment
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        input_file.write(input_yaml)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = f.read()
            
        # Verify all comments are preserved
        assert "# This is a top-level comment" in result
        assert "# This is a meta comment" in result
        assert "# This is a tags comment" in result
        assert "# This is a trailing comment" in result

def test_config_placement_precedence(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'before': 'value',
            'config': {'existing': 'value'},
            'meta': {'owner': 'Team'},
            'tags': ['tag1'],
            'after': 'value'
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = f.read()
            
        # Verify config is placed after 'before' and before 'after'
        before_index = result.find('before:')
        config_index = result.find('config:')
        after_index = result.find('after:')
        
        assert before_index < config_index < after_index

def test_complete_info_preservation(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'meta': {
                'owner': 'Team',
                'description': 'Test model',
                'complex': {
                    'nested': {
                        'value': 42,
                        'list': [1, 2, 3]
                    }
                }
            },
            'tags': ['tag1', 'tag2', 'tag3']
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        # Verify all nested data is preserved
        config = result['models'][0]['config']
        assert config['meta']['owner'] == 'Team'
        assert config['meta']['description'] == 'Test model'
        assert config['meta']['complex']['nested']['value'] == 42
        assert config['meta']['complex']['nested']['list'] == [1, 2, 3]
        assert set(config['tags']) == {'tag1', 'tag2', 'tag3'}

def test_existing_config_preservation(yaml):
    input_data = {
        'models': [{
            'name': 'test_model',
            'config': {
                'custom': 'value',
                'nested': {
                    'key': 'value'
                }
            },
            'meta': {'owner': 'Team'},
            'tags': ['tag1']
        }]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as output_file:
        yaml.dump(input_data, input_file)
        input_file.flush()
        
        transform_yaml(input_file.name, output_file.name)
        
        with open(output_file.name, 'r') as f:
            result = yaml.load(f)
            
        # Verify existing config is preserved
        config = result['models'][0]['config']
        assert config['custom'] == 'value'
        assert config['nested']['key'] == 'value'
        assert config['meta']['owner'] == 'Team'
        assert config['tags'] == ['tag1'] 