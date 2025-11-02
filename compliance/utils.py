import os
import subprocess

def run_cmd(cmd, timeout=10):
    """Run a command and return (rc, stdout, stderr)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"

def is_root():
    return os.geteuid() == 0

def safe_read(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"__ERROR__:{e}"
