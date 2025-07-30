# Configureout

A lightweight and flexible configuration loader for Python. Supports loading configuration from dicts, JSON strings, or files, with namespace-style access.

## Features

- Load config from dict, JSON string, or file
- Automatically converts nested structures to `SimpleNamespace`
- Modify, save, and update configurations easily
- Dictionary-style and attribute-style access
- Prevents reloading after initial load

## Installation

You can install configureout via pip:

```
pip install configureout
```

Or just include `configureout.py` in your project.

## Usage

```python
from configureout import Config

# Load from file
cfg = Config('config.json')

# Or load from dict
cfg = Config({'debug': True, 'db': {'host': 'localhost'}})

#Or load from JSON string
cfg = Config('{"debug": true, "db": {"host": "localhost"}}')

print(cfg.db.host)  # localhost
```

## Public Methods
```python
cfg.to_dict() # Converts the internal namespace config to a standard Python dictionary.

cfg.save(config_path=None, **kwargs) # Saves the current configuration to a JSON file. (Attribute "config_path" is required for non-file configs.)

cfg.update(other=None, **kwargs) # Updates the configuration with new values (from dict or keyword args).

cfg.copy() # Returns a copy of the current configuration.

cfg.keys() / cfg.values() / cfg.items() / cfg.get(key, default=None) # Standard dictionary-style access methods.
```

## Magic Methods
```python
__getitem__(key) / __setitem__(key, value) # Enables dict-style access: cfg['key'].

__delattr__(key) # Deletes a config attribute.

__contains__(key) # Checks if key exists using 'key' in cfg.

__len__() # Returns the number of keys.

__iter__() # Enables iteration over keys.

__str__() # Returns a formatted JSON string of the config.

__repr__() # Developer-friendly representation of the config.

__bool__() # Returns False if the config is empty.

__eq__(other) # Compares config with another Config or dict.

__or__(other) / __ior__(other) # Merge configs using | and |= operators.

__reduce__() # Supports pickling.
```

## Python Version

Python 3.8+ is required.

## License

MIT License