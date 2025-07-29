# CIRCUIT-BREAKER-CLIENT

[![PyPI](https://img.shields.io/pypi/v/circuit-breaker-client.svg)](https://pypi.org/project/circuit-breaker-client/)
[![Python](https://img.shields.io/pypi/pyversions/circuit-breaker-client.svg)](https://pypi.org/project/circuit-breaker-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> A lightweight Python library that provides a simple circuit breaker mechanism for HTTP clients using either `requests`
> or `httpx`.

---

## ✨ Features

- Circuit breaker pattern with failure threshold and recovery timeout
- Support for both `requests` and `httpx`
- Minimal dependencies
- Easily extendable and production-ready

---

## 📦 Installation

Choose the HTTP client you want to use:

### With `requests`:

```bash
pip install circuit-breaker-client[requests]
````

### With `httpx`:

```bash
pip install circuit-breaker-client[httpx]
```

---

## 🚀 Usage

### Using `requests`:

```python
from circuit_breaker_client.requests_client import CircuitBreakerSession

client = CircuitBreakerSession(failure_threshold=3, recovery_timeout=30)

response = client.get("https://httpbin.org/status/200")
print(response.status_code)
```

### Using `httpx`:

```python
from circuit_breaker_client.httpx_client import CircuitBreakerClient

client = CircuitBreakerClient(failure_threshold=3, recovery_timeout=30)

response = client.get("https://httpbin.org/status/200")
print(response.status_code)
```

---

## ⚙️ Parameters

| Parameter           | Description                                     | Default |
|---------------------|-------------------------------------------------|---------|
| `failure_threshold` | Number of consecutive failures to open circuit  | 3       |
| `recovery_timeout`  | Seconds before retrying after circuit is opened | 30      |

---

## 📂 Project Structure

```
circuit-breaker-client/
├── src/
│   └── circuit_breaker_client/
│       ├── __init__.py
│       ├── requests_client.py
│       └── httpx_client.py
├── pyproject.toml
├── README.md
```

---

## 🧪 Development

Install with all optional dependencies:

```bash
poetry install --with requests,httpx
```

---

## 🧪 TestPyPI (optional)

[![TestPyPI](https://img.shields.io/badge/TestPyPI-package-informational)](https://test.pypi.org/project/circuit-breaker-client/)

Install from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ circuit-breaker-client[requests]
```

---

## 📄 License

MIT © Daniel Perebinos
