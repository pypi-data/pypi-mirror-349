# pydantic-core-qpython

This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/pydantic-core/">pydantic-core</a> on <a href="https://www.qpython.org">QPython</a>.

pydantic-core is one of the dependency library of langchain-qpython.

This package provides the core functionality for pydantic validation and serialization.

Pydantic-core is currently around 17x faster than pydantic V1. See tests/benchmarks/ for details.

## Example of direct usage

_NOTE: You should not need to use pydantic-core directly; instead, use pydantic, which in turn uses pydantic-core._

```py
from pydantic_core import SchemaValidator, ValidationError


v = SchemaValidator(
    {
        'type': 'typed-dict',
        'fields': {
            'name': {
                'type': 'typed-dict-field',
                'schema': {
                    'type': 'str',
                },
            },
            'age': {
                'type': 'typed-dict-field',
                'schema': {
                    'type': 'int',
                    'ge': 18,
                },
            },
            'is_developer': {
                'type': 'typed-dict-field',
                'schema': {
                    'type': 'default',
                    'schema': {'type': 'bool'},
                    'default': True,
                },
            },
        },
    }
)

r1 = v.validate_python({'name': 'Samuel', 'age': 35})
assert r1 == {'name': 'Samuel', 'age': 35, 'is_developer': True}

# pydantic-core can also validate JSON directly
r2 = v.validate_json('{"name": "Samuel", "age": 35}')
assert r1 == r2

try:
    v.validate_python({'name': 'Samuel', 'age': 11})
except ValidationError as e:
    print(e)
    """
    1 validation error for model
    age
      Input should be greater than or equal to 18
      [type=greater_than_equal, context={ge: 18}, input_value=11, input_type=int]
    """
```
