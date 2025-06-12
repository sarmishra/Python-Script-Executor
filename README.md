# Safe Script Executor

A secure Flask-based API to run Python scripts inside an isolated sandbox using [nsjail](https://github.com/google/nsjail).

---

## ✅ Requirements

- The input script **must define a `main()` function**, otherwise throw an error
- `main()` **must return a JSON-serializable object**, otherwise throw an error
- Output includes:
  - `result`: the return of `main()`
  - `stdout`: all `print()` output

## ✅ Features

- Runs user-provided Python scripts safely
- Auto-wraps `main()` return to produce valid JSON
- Uses `nsjail` for process isolation
- Lightweight, multi-stage Dockerfile
- Supports local and cloud deployment

---

## 🧪 Local Usage

### Build & Run

```bash
docker build -t safe-script .
docker run --cap-add=SYS_ADMIN --security-opt seccomp=unconfined -p 8080:8080 safe-script
```

### Execute a Script (POST request examples)

```bash
1. curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  print(\"hello world\")\n  return {\"message\": \"done\"}"}'

Response: {"result":{"message":"done"},"stdout":"hello world"}

2. curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  print(\"hello world\")\n "}'

Response: {"error":"main() did not return a value"}

3. curl -X POST http://localhost:8080/execute \                         
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  return {\"message\": \"hello\"}"}'

Response: {"result":{"message":"hello"},"stdout":""}

4. curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "print(\"hello world\")\n  return {\"message\": \"done\"}"}'

Response: {"error":"Script must define a function named main()"}

5. curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  print(\"hello world\")\n  return \"message\""}'

Response: {"error":"main() must return a JSON object (e.g., a Python dict)"}

6. curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  print(\"hello world\")\n  return 1"}'

Response: {"error":"main() must return a JSON object (e.g., a Python dict)"}
```
---

## 📁 Files

- `app.py` – Flask app with `/execute` endpoint
- `executor.py` – Uses `nsjail` to run script in sandbox
- `nsjail.cfg` – Secure jail configuration
- `requirements.txt` – Flask dependency
- `Dockerfile` – 3-stage Docker setup
- `.gitignore` – Common git ignore files
- `.dockerignore` – Common Docker ignore files
