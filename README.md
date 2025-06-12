# Safe Script Executor

A secure Flask-based API to run Python scripts inside an isolated sandbox using [nsjail](https://github.com/google/nsjail).

---

## ✅ Requirements

- The input script **must define a `main()` function**
- `main()` **must return a JSON-serializable object**
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

### Execute a Script

```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  return {\"message\": \"hello\"}"}'
```
`Output:` {"result":{"message":"hello"},"stdout":""}
---

## 📁 Files

- `app.py` – Flask app with `/execute` endpoint
- `executor.py` – Uses `nsjail` to run script in sandbox
- `nsjail.cfg` – Secure jail configuration
- `requirements.txt` – Flask dependency
- `Dockerfile` – 3-stage Docker setup
- `.gitignore` – Common git ignore files
- `.dockerignore` – Common Docker ignore files
