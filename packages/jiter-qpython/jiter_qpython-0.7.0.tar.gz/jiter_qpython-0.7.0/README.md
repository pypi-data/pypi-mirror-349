This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/jiter/">jiter</a> on <a href="https://www.qpython.org">QPython</a>.

This is a standalone version of the JSON parser used in `pydantic-core`. The recommendation is to only use this package directly if you do not use `pydantic`.

## Examples

The main function provided by Jiter is `from_json()`, which accepts a bytes object containing JSON and returns a Python dictionary, list or other value.

```python
from jiter import from_json

json_data = b'{"name": "John", "age": 30}'
parsed_data = jiter.from_json(json_data)
print(parsed_data)  # Output: {'name': 'John', 'age': 30}
```

## Handling Partial JSON

Incomplete JSON objects can be parsed using the `partial_mode=` parameter.

```python
import jiter

partial_json = b'{"name": "John", "age": 30, "city": "New Yor'

# Raise error on incomplete JSON
try:
    jiter.from_json(partial_json, partial_mode=False)
except ValueError as e:
    print(f"Error: {e}")

# Parse incomplete JSON, discarding incomplete last field
result = jiter.from_json(partial_json, partial_mode=True)
print(result)  # Output: {'name': 'John', 'age': 30}

# Parse incomplete JSON, including incomplete last field
result = jiter.from_json(partial_json, partial_mode='trailing-strings')
print(result)  # Output: {'name': 'John', 'age': 30, 'city': 'New Yor'}
```