# Python Function Signatures and API Design

**Project Orion Handbook — Core Python**

> This chapter records the deep-dive material from Sprint 02 on Python function parameters, signatures, argument binding, introspection, and API design.

---

## 1. Why This Topic Matters

Beginner Python courses usually teach how to define and call functions.

For professional Python development, it is equally important to understand the function's **contract**:

- how arguments are matched to parameters,
- what kinds of parameters Python supports,
- why some arguments must be positional or keyword-only,
- how Python reports invalid calls,
- how function signatures can be inspected at runtime,
- and how frameworks use this information.

The central idea is:

> **A function signature is part of the API, not merely an implementation detail.**

---

# 2. A Function Call Is a Negotiation

Consider:

```python
def write_inventory(data, output_file="inventory.json"):
    ...
```

and:

```python
write_inventory(inventory)
```

Conceptually, Python performs these stages:

```text
Caller
  |
  | arguments
  v
Function object
  |
  | signature
  v
Parameter binding
  |
  v
Function execution
```

The important point is that **parameter binding occurs before the function body executes**.

Python first determines whether the supplied arguments can legally be matched to the function's parameters.

If binding fails, a `TypeError` is raised and the function body is never entered.

---

# 3. Argument Binding

Given:

```python
def add(a, b):
    return a + b
```

## Missing argument

```python
add(5)
```

Conceptually:

```text
a = 5
b = ?
```

Python raises a missing-argument `TypeError`.

## Normal positional binding

```python
add(5, 10)
```

becomes:

```text
a = 5
b = 10
```

## Keyword binding

```python
add(5, b=10)
```

also becomes:

```text
a = 5
b = 10
```

## Multiple values

```python
add(5, a=10)
```

attempts:

```text
a = 5
a = 10
```

Python therefore raises a `TypeError` for multiple values for `a`.

## Unexpected keyword

```python
add(x=5, y=10)
```

The function has parameters named `a` and `b`, not `x` and `y`.

Python therefore raises an unexpected-keyword `TypeError`.

---

# 4. The Errors Are All Part of the Same Mechanism

These errors:

- missing required argument,
- multiple values for an argument,
- unexpected keyword argument,
- too many positional arguments,

are different failures of the **argument-binding process**.

This explains the error encountered while refactoring `write_inventory()`:

```text
TypeError: write_inventory() got an unexpected keyword argument 'output_file'
```

The caller used:

```python
write_inventory(
    inventory,
    output_file="inventory.json",
)
```

but the function originally accepted only something equivalent to:

```python
def write_inventory(data):
    ...
```

There was no `output_file` parameter in the signature, so binding failed before the function body executed.

---

# 5. The Five Parameter Kinds

Python has five parameter categories.

A deliberately comprehensive example is:

```python
def f(
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

The categories are:

1. `POSITIONAL_ONLY`
2. `POSITIONAL_OR_KEYWORD`
3. `VAR_POSITIONAL`
4. `KEYWORD_ONLY`
5. `VAR_KEYWORD`

These are represented explicitly by Python's introspection machinery.

---

# 6. Positional-Only Parameters

The `/` separator marks parameters before it as positional-only.

```python
def f(a, b, /):
    ...
```

Legal:

```python
f(10, 20)
```

Not legal:

```python
f(a=10, b=20)
```

## Why use positional-only parameters?

Sometimes the parameter name is an implementation detail and should not become part of the public API.

This gives library authors more freedom to change internal parameter names later.

Python's built-in APIs use positional-only parameters in many places.

The important design idea is:

> **If callers should care about the value but not the parameter name, positional-only can protect the API from unnecessary coupling.**

---

# 7. Positional-or-Keyword Parameters

These are the familiar parameters:

```python
def connect(host, port):
    ...
```

Both are valid:

```python
connect("db01", 3306)
```

and:

```python
connect(host="db01", port=3306)
```

This is the most common parameter category.

---

# 8. Variable Positional Parameters

```python
def f(*args):
    ...
```

Extra positional arguments are collected into a tuple.

```python
f(1, 2, 3, 4)
```

Inside the function:

```python
args == (1, 2, 3, 4)
```

The important professional-level point is that `*args` is not simply "extra arguments"; it is a parameter with the explicit kind:

```python
inspect.Parameter.VAR_POSITIONAL
```

---

# 9. Keyword-Only Parameters

The `*` separator can force following parameters to be supplied by keyword.

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
connect(
    "db01",
    timeout=30,
    retries=5,
)
```

Invalid:

```python
connect(
    "db01",
    30,
    5,
)
```

## Why is this useful?

Compare:

```python
connect("db01", 30, 5)
```

with:

```python
connect(
    "db01",
    timeout=30,
    retries=5,
)
```

The second form is much more self-documenting.

Keyword-only parameters are therefore an important **API design tool**, not merely a syntax feature.

---

# 10. Variable Keyword Parameters

```python
def f(**kwargs):
    ...
```

Extra keyword arguments are collected into a dictionary.

```python
f(
    timeout=30,
    retries=5,
)
```

Inside:

```python
kwargs == {
    "timeout": 30,
    "retries": 5,
}
```

The parameter kind is:

```python
inspect.Parameter.VAR_KEYWORD
```

---

# 11. Reading a Complex Signature

Consider:

```python
def connect(
    host,
    /,
    port=3306,
    *,
    timeout=30,
    ssl=True,
    **kwargs,
):
    ...
```

Read it as:

```text
host
    positional-only

port
    positional-or-keyword

timeout
    keyword-only

ssl
    keyword-only

kwargs
    variable keyword arguments
```

The signature itself communicates how the API is intended to be used.

---

# 12. `json.dump()` as a Real-World Example

A signature similar to:

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

contains `*`.

Therefore the parameters after `*` are keyword-only.

This makes calls such as:

```python
json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False,
)
```

clear and intentional.

---

# 13. The `Path.open()` vs `json.dump()` Lesson

This connects directly to an earlier Orion debugging session.

This was incorrect:

```python
output_file.open(
    "w",
    encoding="utf-8",
    ensure_ascii=False,
)
```

because `ensure_ascii` is not a parameter of `Path.open()`.

The correct place for `ensure_ascii` is `json.dump()`:

```python
json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False,
)
```

The two functions have different signatures.

Therefore they accept different keyword arguments.

The lesson is:

> **A keyword argument is not globally valid in Python. It is valid only if the receiving function's signature accepts it.**

---

# 14. Function Introspection

Python functions are objects.

They carry metadata.

Example:

```python
def add(a: int, b: int = 10) -> int:
    """Add two numbers."""
    return a + b
```

The function object exposes information such as:

```python
add.__name__
add.__doc__
add.__annotations__
```

For example:

```python
print(add.__name__)
```

returns:

```text
add
```

and:

```python
print(add.__doc__)
```

returns:

```text
Add two numbers.
```

and:

```python
print(add.__annotations__)
```

contains the annotations.

---

# 15. `inspect.signature()`

Python's `inspect` module provides a high-level way to inspect a function's signature.

```python
import inspect

print(inspect.signature(add))
```

Output:

```text
(a: int, b: int = 10) -> int
```

The returned object is an:

```python
inspect.Signature
```

object.

Example:

```python
signature = inspect.signature(add)

print(type(signature))
```

---

# 16. Inspecting Individual Parameters

```python
for name, parameter in signature.parameters.items():
    print(name, parameter)
```

A parameter is itself an object.

You can inspect:

```python
parameter.name
parameter.kind
parameter.default
```

For example:

```python
for parameter in signature.parameters.values():
    print(
        parameter.name,
        parameter.kind,
        parameter.default,
    )
```

---

# 17. Parameter Kinds Are Explicit Runtime Objects

Python exposes the parameter categories through `inspect.Parameter`:

```python
inspect.Parameter.POSITIONAL_ONLY
inspect.Parameter.POSITIONAL_OR_KEYWORD
inspect.Parameter.VAR_POSITIONAL
inspect.Parameter.KEYWORD_ONLY
inspect.Parameter.VAR_KEYWORD
```

Example:

```python
import inspect

def connect(
    host,
    /,
    port=3306,
    *,
    timeout=30,
    **kwargs,
):
    pass

sig = inspect.signature(connect)

for parameter in sig.parameters.values():
    print(parameter.name, parameter.kind)
```

This allows Python programs and frameworks to reason about function APIs programmatically.

---

# 18. Explicit Argument Binding with `Signature.bind()`

`inspect.Signature` can model the argument-binding process.

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

The resulting mapping contains the arguments that were explicitly bound:

```python
{
    "host": "mysql01",
    "timeout": 10,
}
```

This lets tooling work with a function's calling contract without executing the function.

---

# 19. `bind()` vs `bind_partial()`

Consider:

```python
def connect(host, port):
    pass
```

This is incomplete:

```python
sig.bind("mysql01")
```

because `port` is required.

But:

```python
sig.bind_partial("mysql01")
```

allows the partial binding.

This distinction is useful to frameworks and tools that construct calls incrementally.

---

# 20. Function Decorators and Signatures

A decorator can replace a function with another function.

Example:

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper
```

The wrapper's visible signature is:

```python
(*args, **kwargs)
```

That can hide useful information about the original function.

Use:

```python
from functools import wraps
```

and:

```python
def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper
```

`functools.wraps` preserves important metadata and helps introspection tools follow the wrapped function.

This is important for frameworks and tooling.

---

# 21. Why Frameworks Can Inspect Functions

Many Python frameworks and tools use function metadata and signatures.

A general pattern is:

```text
Python function
       |
       v
Introspection
       |
       +-- name
       +-- signature
       +-- annotations
       +-- defaults
       +-- metadata
       |
       v
Framework/tool behavior
```

This is part of why systems such as:

- FastAPI
- pytest
- Click/Typer
- Django tooling

can build behavior around user-defined functions.

The exact mechanisms differ by framework; the important general concept is **runtime introspection**.

---

# 22. Type Hints Are Metadata

Consider:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Python stores the annotations.

But Python does not automatically enforce that:

```python
add("hello", "world")
```

is invalid simply because the parameters were annotated as `int`.

A framework or external tool may interpret the annotations and enforce rules.

Therefore distinguish:

```text
Python
  |
  +-- stores annotations

Framework / tool
  |
  +-- interprets annotations
```

This connects directly to our earlier Orion deep dive on type hints.

---

# 23. Function Signatures as API Design

Consider:

```python
def write_inventory(data, output_file):
    ...
```

A stronger API can be:

```python
def write_inventory(
    data: dict[str, Any],
    *,
    output_file: str = "inventory.json",
    pretty: bool = False,
) -> None:
    ...
```

Now the API communicates:

- `data` is the primary input.
- `output_file` is an optional configuration.
- `pretty` is an optional configuration.
- configuration arguments must be explicit keywords.

A caller writes:

```python
write_inventory(
    inventory,
    output_file="server01.json",
    pretty=True,
)
```

rather than:

```python
write_inventory(
    inventory,
    "server01.json",
    True,
)
```

The first form is harder to misuse and easier to understand later.

---

# 24. API Stability

A function signature is also an API compatibility boundary.

Suppose users have written:

```python
write_inventory(data, "server01.json")
```

Changing:

```python
def write_inventory(data, output_file):
```

to:

```python
def write_inventory(data, *, output_file):
```

would break those callers.

Therefore signature design has consequences beyond the current implementation.

When designing public APIs, ask:

> "How do I want users to call this function today, and how much freedom do I want to retain to change it later?"

This is why positional-only and keyword-only parameters are powerful API-design mechanisms.

---

# 25. The Larger Mental Model

Several Python concepts that initially seem unrelated are actually connected:

```text
Functions are objects
        |
        v
Functions carry metadata
        |
        +-- __name__
        +-- __doc__
        +-- __annotations__
        +-- defaults
        +-- signature information
        |
        v
inspect module
        |
        v
Parameter objects
        |
        v
Argument binding
        |
        v
Frameworks and developer tooling
```

This is a major part of Python's flexibility.

---

# 26. Orion Engineering Principles

### Principle 23

> **Every function call is a contract between the caller and the function signature.**

The caller supplies arguments.

The signature determines whether those arguments can legally bind.

Only after successful binding does the function body execute.

### Principle 24

> **A function signature is part of the API, not merely an implementation detail.**

A good signature communicates intended usage and helps prevent ambiguity.

### Principle 25

> **Use introspection to understand an unfamiliar Python API instead of relying exclusively on memorization or examples.**

Useful tools include:

```python
help()
dir()
inspect.signature()
inspect.Parameter
```

---

# 27. Practical Investigation Pattern

When you encounter an unfamiliar function:

### First

```python
help(function)
```

### Then

```python
import inspect

inspect.signature(function)
```

### Then inspect annotations if useful:

```python
function.__annotations__
```

### Then perform a small experiment.

This is often faster and more reliable than guessing.

For example, when wondering whether a function supports:

```python
ensure_ascii=False
```

inspect its signature rather than trying random arguments.

---

# 28. Orion's Practical Rule

When you see unfamiliar Python code such as:

```python
some_function(
    value,
    option=True,
    timeout=30,
)
```

don't think:

> "I don't remember this syntax."

Instead ask:

1. What is the function object?
2. What is its signature?
3. Which parameters are positional-only?
4. Which are positional-or-keyword?
5. Which are keyword-only?
6. What are the defaults?
7. What does the function return?
8. What does its documentation say?

That mindset turns unfamiliar Python code from something intimidating into something you can systematically investigate.

---

## Quick Reference

```text
/       → marks the end of positional-only parameters

*       → marks the beginning of keyword-only parameters
          when *args is not present

*args   → variable positional parameters

**kwargs → variable keyword parameters

inspect.signature()
        → inspect a function's signature

Signature.bind()
        → model argument binding

Signature.bind_partial()
        → allow incomplete binding

__annotations__
        → access function annotations

__defaults__
        → positional/default parameter values

__kwdefaults__
        → keyword-only default values

functools.wraps
        → preserve important wrapped-function metadata
```

---

## Suggested repository location

```text
handbook/
└── PYTHON_FUNCTION_SIGNATURES_AND_API_DESIGN.md
```

This chapter should remain a reference document rather than something you need to memorize. The goal is that when you encounter a strange signature or a `TypeError` months from now, you can return here and immediately reconstruct what Python is doing.
