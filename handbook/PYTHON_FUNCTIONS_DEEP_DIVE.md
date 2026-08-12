# Python Functions — Deep Dive Reference

**Project Orion Handbook — Sprint 02**

This document consolidates the deeper Python function concepts covered during Sprint 02. It is a long-term reference for reading unfamiliar Python code, debugging `TypeError` messages, and designing application APIs.

## 1. Functions Are Objects

In Python, a function is an object.

```python
def greet(name):
    return f"Hello {name}"

print(greet)
```

`greet` refers to the function object, while `greet()` calls the function.

```text
greet     → function object
greet()   → function call
```

Because functions are objects, they can be assigned to variables, passed to other functions, returned from functions, stored in collections, and inspected at runtime.

This is foundational to decorators and callback-based APIs.

## 2. A Function Call Is an Argument-Binding Process

Given:

```python
def add(a, b):
    return a + b
```

Python first binds arguments to parameters:

```text
a → 10
b → 20
```

Only after successful binding does the function body execute.

Examples:

```python
add(10)              # missing argument
add(10, a=20)        # multiple values for a
add(x=10, y=20)      # unexpected keywords
```

These are failures of the argument-binding process.

> **Many function-call `TypeError`s happen before the function body executes.**

## 3. The Five Parameter Kinds

Python has five parameter categories:

1. `POSITIONAL_ONLY`
2. `POSITIONAL_OR_KEYWORD`
3. `VAR_POSITIONAL`
4. `KEYWORD_ONLY`
5. `VAR_KEYWORD`

A comprehensive signature can contain several:

```python
def example(
    a,
    b,
    /,
    c,
    d=10,
    *args,
    e,
    f=20,
    **kwargs,
):
    ...
```

These categories are represented by `inspect.Parameter` objects.

## 4. Positional-Only Parameters

`/` marks parameters before it as positional-only:

```python
def f(a, b, /):
    ...
```

Valid:

```python
f(10, 20)
```

Invalid:

```python
f(a=10, b=20)
```

This is useful when callers should depend on the values and their positions, but not on parameter names.

> **Positional-only parameters can protect parameter names from becoming API commitments.**

## 5. Positional-or-Keyword Parameters

Normal parameters are positional-or-keyword:

```python
def connect(host, port):
    ...
```

Both are valid:

```python
connect("db01", 3306)
connect(host="db01", port=3306)
```

## 6. Variable Positional Parameters — `*args`

```python
def f(*args):
    ...
```

Extra positional arguments are collected into a tuple:

```python
f(1, 2, 3, 4)
```

Inside:

```python
args == (1, 2, 3, 4)
```

The formal parameter kind is:

```python
inspect.Parameter.VAR_POSITIONAL
```

## 7. Keyword-Only Parameters

A bare `*` makes following parameters keyword-only:

```python
def connect(
    host,
    *,
    timeout,
    retries,
):
    ...
```

Valid:

```python
connect("db01", timeout=30, retries=5)
```

Invalid:

```python
connect("db01", 30, 5)
```

Keyword-only parameters are especially useful for configuration because the call site becomes self-documenting.

## 8. Variable Keyword Parameters — `**kwargs`

```python
def f(**kwargs):
    ...
```

Extra keyword arguments are collected into a dictionary:

```python
f(timeout=30, retries=5)
```

Inside:

```python
kwargs == {
    "timeout": 30,
    "retries": 5,
}
```

The formal parameter kind is:

```python
inspect.Parameter.VAR_KEYWORD
```

## 9. Defaults Are Part of the API

```python
def write_inventory(
    data,
    *,
    pretty=False,
):
    ...
```

Calling:

```python
write_inventory(data)
```

means `pretty=False`.

Changing a default can change application behavior even if the signature otherwise remains compatible.

> **Default values are part of a function's behavioral contract.**

## 10. Mutable Default Arguments

Avoid:

```python
def collect(items=[]):
    items.append("cpu")
    return items
```

The default list is created when the function is defined, not each time it is called.

Safer:

```python
def collect(items=None):
    if items is None:
        items = []

    items.append("cpu")
    return items
```

The deeper principle is:

> **Default expressions are evaluated when the function definition executes.**

This connects function signatures directly to Python's object model.

## 11. Function Metadata

Functions are objects and carry metadata:

```python
def add(a: int, b: int = 10) -> int:
    return a + b
```

Useful attributes include:

```python
add.__name__
add.__doc__
add.__annotations__
```

Defaults are also stored:

```python
add.__defaults__
add.__kwdefaults__
```

The latter is specifically for keyword-only defaults.

## 12. `inspect.signature()`

Python's standard library provides runtime introspection:

```python
import inspect

def add(a: int, b: int = 10) -> int:
    return a + b

signature = inspect.signature(add)

print(signature)
```

Output:

```text
(a: int, b: int = 10) -> int
```

The result is an `inspect.Signature` object.

## 13. Inspecting Individual Parameters

A signature contains parameter objects:

```python
for name, parameter in signature.parameters.items():
    print(name, parameter)
```

Useful attributes include:

```python
parameter.name
parameter.kind
parameter.default
```

Parameter kinds are available as:

```python
inspect.Parameter.POSITIONAL_ONLY
inspect.Parameter.POSITIONAL_OR_KEYWORD
inspect.Parameter.VAR_POSITIONAL
inspect.Parameter.KEYWORD_ONLY
inspect.Parameter.VAR_KEYWORD
```

This makes parameter categories available to Python programs and tooling at runtime.

## 14. `Signature.bind()`

`Signature` can model argument binding:

```python
def connect(host, port=3306, *, timeout=30):
    pass

sig = inspect.signature(connect)

bound = sig.bind(
    "mysql01",
    timeout=10,
)

print(bound.arguments)
```

The resulting mapping represents the successful binding:

```python
{
    "host": "mysql01",
    "timeout": 10,
}
```

This lets tools reason about calls without executing the function.

## 15. `bind()` vs `bind_partial()`

Given:

```python
def connect(host, port):
    pass
```

This fails because `port` is required:

```python
sig.bind("mysql01")
```

But:

```python
sig.bind_partial("mysql01")
```

allows incomplete binding.

This is useful for tools and frameworks that construct calls incrementally.

## 16. Type Hints Are Metadata

```python
def add(a: int, b: int) -> int:
    return a + b
```

Python stores these annotations, but does not automatically enforce them.

The distinction is:

```text
Python
    stores annotations

Tools / frameworks
    may interpret annotations
    and perform validation or other behavior
```

This connects directly to our earlier deep dive on type hints.

## 17. Decorators Can Hide Signatures

A decorator may replace a function with a wrapper:

```python
def logger(func):

    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper
```

The wrapper's own signature is `(*args, **kwargs)`, which can obscure useful metadata.

Use:

```python
from functools import wraps

def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper
```

`functools.wraps` preserves important wrapped-function metadata and helps introspection tools follow the original function.

## 18. Why Frameworks Can Inspect Functions

Python allows tools and frameworks to inspect:

```text
function
    │
    ├── name
    ├── documentation
    ├── annotations
    ├── defaults
    └── signature
            │
            ▼
       introspection
            │
            ▼
    framework/tool behavior
```

The exact mechanisms differ by framework, but the underlying capability is Python runtime introspection.

## 19. API Design: Start With the Call Site

Less readable:

```python
write_inventory(
    inventory,
    "server01.json",
    True,
)
```

More readable:

```python
write_inventory(
    inventory,
    output_file="server01.json",
    pretty=True,
)
```

The second call communicates intent without requiring the reader to look up the signature.

> **Design functions from the caller's perspective.**

## 20. Primary Inputs vs Configuration

A good design might be:

```python
def write_inventory(
    data,
    *,
    output_file="inventory.json",
    pretty=False,
):
    ...
```

Here:

```text
data
    primary input

output_file
pretty
    configuration
```

Keyword-only parameters naturally distinguish configuration from primary data.

## 21. Positional Arguments Are an API Commitment

If an API exposes:

```python
def connect(host, port):
    ...
```

callers can write:

```python
connect("db01", 3306)
```

The API has committed to the positional meaning of those arguments.

A more explicit design can be:

```python
def connect(
    host,
    *,
    port=3306,
):
    ...
```

Now:

```python
connect("db01", port=3306)
```

is clearer and can be easier to evolve.

## 22. Positional-Only Has the Opposite Goal

```text
POSITIONAL_ONLY
    Protects parameter names from becoming API commitments.

KEYWORD_ONLY
    Makes configuration explicit and named.
```

These solve different API-design problems.

## 23. Don't Put Everything Into `**kwargs`

This is tempting:

```python
def write_inventory(data, **kwargs):
    ...
```

But it hides the supported API.

A typo such as:

```python
write_inventory(
    data,
    output_fil="server.json",
)
```

can be harder to detect if arbitrary keywords are accepted.

Prefer:

```python
def write_inventory(
    data,
    *,
    output_file="inventory.json",
):
    ...
```

for known options.

> **Use explicit parameters for known API options. Use `**kwargs` when arbitrary extension or forwarding is intentionally part of the design.**

## 24. `**kwargs` for Forwarding

A legitimate use is an adapter:

```python
def my_json_dump(data, **kwargs):
    return json.dump(data, **kwargs)
```

Here `kwargs` deliberately forwards options.

If the wrapper has a known stable interface, explicit parameters can provide better documentation and validation.

## 25. API Evolution

Suppose version 1 has:

```python
def write_inventory(data, output_file):
    ...
```

Later you need:

```text
pretty
compress
overwrite
```

A useful evolution is:

```python
def write_inventory(
    data,
    output_file,
    *,
    pretty=False,
    compress=False,
    overwrite=False,
):
    ...
```

Existing calls can continue working while new optional behavior is introduced as keyword-only configuration.

> **Keyword-only parameters provide a useful place for future optional behavior.**

## 26. Narrow Interfaces

Avoid exposing controls callers do not genuinely need.

Prefer:

```python
def write_inventory(
    data,
    *,
    output_file="inventory.json",
    pretty=False,
):
    ...
```

over:

```python
def process_everything(data, **kwargs):
    ...
```

Narrow interfaces are generally easier to understand, test, use correctly, and evolve.

## 27. `json.dump()` as a Real-World Example

A simplified view of its API is:

```python
json.dump(
    obj,
    fp,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
)
```

The important design pattern is:

```text
Primary inputs
    obj
    fp

Behavior/configuration
    indent
    ensure_ascii
    sort_keys
    default
    ...
```

This is why:

```python
json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False,
)
```

is clear.

## 28. `Path.open()` vs `json.dump()`

This connects directly to an Orion debugging incident.

Incorrect:

```python
output_file.open(
    "w",
    encoding="utf-8",
    ensure_ascii=False,
)
```

`ensure_ascii` is not a parameter of `Path.open()`.

It belongs to JSON serialization:

```python
json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False,
)
```

> **A keyword argument is valid only if the receiving function's API accepts it.**

When you see:

```text
TypeError: ... got an unexpected keyword argument ...
```

inspect the receiving function's signature.

## 29. Separation of Responsibilities

If a function's responsibility is collecting system information, it should ideally not also decide where that information is written.

Prefer:

```python
def collect_system(
    *,
    network=False,
    disk=False,
    memory=True,
    cpu=True,
) -> dict:
    ...
```

and:

```python
def write_inventory(
    data,
    *,
    output_file="output.json",
    pretty=False,
) -> None:
    ...
```

The flow is:

```text
collect_system()
       │
       ▼
   inventory
       │
       ▼
write_inventory()
       │
       ▼
 output.json
```

This is separation of concerns.

## 30. CLI and Function APIs

CLI:

```bash
uv run main.py --output server01.json --pretty
```

Python:

```python
write_inventory(
    inventory,
    output_file="server01.json",
    pretty=True,
)
```

Conceptually:

```text
Human
  │
  ▼
CLI arguments
  │
  ▼
Application configuration
  │
  ▼
Python function parameters
  │
  ▼
Application logic
```

Good architecture prevents CLI-specific details from leaking unnecessarily into core application functions.

## 31. Avoid Over-Engineering

It is possible to expose too many options:

```python
def write_inventory(
    data,
    *,
    output_file="inventory.json",
    pretty=False,
    compress=False,
    encoding="utf-8",
    overwrite=True,
    backup=False,
    timestamp=False,
):
    ...
```

The fact that an option can exist does not mean it should exist.

Ask:

> **What behavior does the application actually need?**

Good API design includes restraint.

## 32. Function Signatures as Documentation

Consider:

```python
def write_inventory(
    data: dict[str, object],
    *,
    output_file: str = "inventory.json",
    pretty: bool = False,
) -> None:
    ...
```

Before reading the implementation, a developer can infer:

- the primary input is `data`,
- the function returns `None`,
- the output filename is optional,
- pretty-printing is optional,
- configuration must be supplied by keyword.

A good signature communicates intent before the implementation does.

## 33. Professional Function-Design Checklist

Before finalizing a function, ask:

1. What is the primary input?
2. Which parameters are configuration?
3. Should each parameter be positional, positional-or-keyword, or keyword-only?
4. Should callers depend on the parameter names?
5. Are the defaults safe and intuitive?
6. Could a mutable default object accidentally be shared?
7. Do arbitrary positional arguments genuinely make sense?
8. Is arbitrary keyword forwarding or extension intentional?
9. Are all exposed options actually needed?
10. How might the signature change later?
11. Does the function have one focused responsibility?

## 34. The Mental Model

```text
Functions are objects
        │
        ▼
Functions carry metadata
        │
        ├── name
        ├── documentation
        ├── annotations
        ├── defaults
        └── signature
        │
        ▼
inspect module
        │
        ▼
Parameter objects
        │
        ▼
Argument binding
        │
        ▼
TypeError when binding fails
        │
        ▼
Function/API design
        │
        ▼
Frameworks and developer tooling
```

The syntax (`/`, `*`, `*args`, `**kwargs`) is only the visible part.

The deeper subject is:

> **Python provides precise, inspectable function contracts that can be used to build maintainable APIs and sophisticated tooling.**

## 35. Orion Engineering Principles

### Principle 23 — Function Calls Are Contracts

> **Every function call is a contract between the caller and the function signature.**

The caller supplies arguments. The signature determines whether those arguments can legally bind. Only after successful binding does the function body execute.

### Principle 24 — Signatures Are APIs

> **A function signature is part of the API, not merely an implementation detail.**

Parameter names, kinds, defaults, and return annotations communicate intended usage.

### Principle 25 — Inspect Before Guessing

> **Use introspection to understand an unfamiliar Python API instead of relying exclusively on memorization.**

Useful tools include:

```python
help(function)
inspect.signature(function)
function.__annotations__
function.__defaults__
function.__kwdefaults__
```

### Principle 26 — Prefer Explicit Interfaces

> **Use explicit parameters for known API options; use `*args` and `**kwargs` only when variable arguments are intentionally part of the interface.**

### Principle 27 — Separate Responsibilities

> **A function should have a focused responsibility, and its parameters should reflect that responsibility.**

For example:

```text
collect_system()
    → collect information

write_inventory()
    → serialize and write information
```

## 36. Quick Reference

```text
/                    → ends positional-only parameters

*                    → begins keyword-only parameters
                       when *args is not present

*args                → variable positional parameters

**kwargs             → variable keyword parameters

inspect.signature()  → inspect a function's signature

Signature.bind()     → model normal argument binding

Signature.bind_partial()
                     → allow incomplete binding

__annotations__      → access function annotations

__defaults__         → ordinary positional/default values

__kwdefaults__       → keyword-only defaults

functools.wraps      → preserve important wrapped-function metadata
```

## Final Takeaway

The goal is not to memorize every form of Python function syntax.

The goal is to be able to look at an unfamiliar signature such as:

```python
def process(
    data,
    /,
    limit=100,
    *items,
    timeout=30,
    **options,
):
    ...
```

and immediately ask:

1. Which arguments are positional-only?
2. Which are positional-or-keyword?
3. Which are variable positional?
4. Which are keyword-only?
5. Which are variable keyword?
6. What are the defaults?
7. What is the API trying to communicate?
8. How can I inspect it rather than guess?

Once those questions become natural, complex Python signatures stop looking like advanced Python magic and become readable API contracts.
