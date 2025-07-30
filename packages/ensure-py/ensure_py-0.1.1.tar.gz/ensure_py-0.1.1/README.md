# ensure-py

Repair and parse "almost-JSON" from LLMs (like GPT, Claude) into valid Python objects, or raise a clear error. Works in any Python 3.7+ environment. Zero dependencies (Pydantic optional for schema validation).

---

## Install

```bash
pip install ensure-py
```

---

## Usage

### As a Python Library

```python
from ensure_json import ensure_json, JsonFixError

try:
    obj = ensure_json('{ name: "Alice", age: 42, }')
    print(obj)  # {'name': 'Alice', 'age': 42}
except JsonFixError as err:
    print("Could not parse JSON:", err)
```

#### With Pydantic Schema (optional)

```python
from ensure_json import ensure_json
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = ensure_json('{ name: "Alice", age: 42 }', schema=User)
print(user)  # User(name='Alice', age=42)
```

### Command Line

```bash
echo '{ name: "Alice", age: 42, }' | ensure-json
# or
echo '{ name: "Alice", age: 42, }' | python -m ensure_py.cli
```

---

## Features

- Repairs and parses "almost-JSON" from LLMs (extra commas, unquoted keys, etc.)
- Returns a valid Python object or raises `JsonFixError`
- Optional Pydantic schema validation
- Minimal CLI for quick fixes
- No dependencies required (Pydantic optional)

---

## License

MIT
