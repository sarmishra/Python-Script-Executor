import json
import subprocess
import tempfile
import os
import ast


def contains_main_function(code: str) -> bool:
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                return True
    except SyntaxError:
        return False
    return False


def execute_script(user_code):
    if not contains_main_function(user_code):
        raise Exception("Script must define a function named main()")

    # Patch script to serialize main() return
    wrapped_code = f"{user_code.strip()}\nimport json\nprint(json.dumps(main()))"

    with tempfile.NamedTemporaryFile(delete=False, dir='/app', suffix='.py') as f:
        f.write(wrapped_code.encode())
        f.flush()
        os.chmod(f.name, 0o444)  # make it read-only

        command = [
            "nsjail",
            "--config", "nsjail.cfg",
            "--",
            "/usr/bin/python", f.name
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, timeout=10
        )

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()

        if process.returncode != 0:
            raise Exception(f"Script execution failed: {stderr}")

        lines = stdout.splitlines()
        for line in reversed(lines):
            try:
                result_json = json.loads(line)
                if result_json is None:
                    raise Exception("main() did not return a value")
                if not isinstance(result_json, dict):
                    raise Exception("main() must return a JSON object (e.g., a Python dict)")
                return result_json, "\n".join(lines[:-1])
            except json.JSONDecodeError:
                continue

        raise Exception("Script did not return valid JSON from main()")