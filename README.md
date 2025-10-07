---
theme: "black"
transition: "slide"
progress: false
slideNumber: false
title: Thomas Pohl - Trainer Profile
customTheme: "tom"
---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;700&family=Titillium+Web:wght@300&display=swap" rel="stylesheet">

# Workshop on `asyncio` in Python
September 8, 2025

---

## Why asyncio?

--

## Multi-Processing / Multi-Threading

Complex and error-prone

--

## I/O is slow

Typical network request: 10 ... 100 ms

⬇

50 000 000 ... 500 000 000 cycles for 5 GHz CPU

--

## Save you from _callback hell_

```python
def handle_callback(request):
    # what's the context?
    return "something"

def main():
    context = "hello world"
    server = Server()
    server.register_callback(handle_callback)
    ...
```


--

## Humans work asyncronously, too

Our brains cannot handle _multi-processing_ really well.

---

## How does `asyncio` work?

--

## Your to-do list
* Book dentist appointment
* Support dad with computer issue
* Reserve table at restaurant

All tasks involve **communication** (aka I/O).{.fragment}

---

## Useful libraries

**`asyncio` Alternatives**
* https://github.com/dabeaz/curio (EOL)
* https://github.com/python-trio/trio
* https://github.com/agronholm/anyio

**Better QoL with `asyncio`**
* https://github.com/Tinche/quattro
* https://github.com/x42005e1f/aiologic (low bus factor)
