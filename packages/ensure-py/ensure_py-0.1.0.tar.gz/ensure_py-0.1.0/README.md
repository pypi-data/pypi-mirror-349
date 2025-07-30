# ensure-py

A <3kB, dependency-free Python toolkit to repair "almost-JSON" text from LLMs and return a valid Python object—or raise `JsonFixError`.

## Install

```bash
pip install .
# or, for development:
pip install -e .
```

## Usage

### Programmatic

```python
from ensure_py import ensure_json, JsonFixError

try:
    obj = ensure_json('{ name: "Alice", age: 42, }')
    # obj: {'name': 'Alice', 'age': 42}
except JsonFixError as err:
    # handle error, maybe re-prompt LLM
    print(err)
```

### With Pydantic Schema

```python
from ensure_py import ensure_json
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

obj = ensure_json('{ name: "Alice", age: 42 }', schema=User)
# obj: User(name='Alice', age=42)
```

### Async

```python
from ensure_py import ensure_json_async
import asyncio

result = asyncio.run(ensure_json_async('{ name: "Alice" }'))
```

### CLI

```bash
echo '{ name: "Alice", age: 42, }' | python -m ensure_py.cli
# { "name": "Alice", "age": 42 }
```

Show help:

```bash
python -m ensure_py.cli --help
```

## API

- `ensure_json(raw: str, schema=None) -> Any`
- `ensure_json_async(raw: str, schema=None) -> Awaitable[Any]`
- `JsonFixError` (includes `.raw` property)

## Features

- Repairs and parses "almost-JSON" from LLMs (GPT, Claude, etc.)
- Works in any Python 3.7+ environment
- Sync & async API
- Optional Pydantic schema validation
- Minimal CLI
- Zero dependencies (Pydantic optional)

## License

MIT
